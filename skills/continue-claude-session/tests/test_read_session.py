import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "read_session.py"
spec = importlib.util.spec_from_file_location("reader", SCRIPT)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / "project"
        self.project.mkdir()
        self.path = self.write("a", "session-a", self.project, "2026-01-01T00:00:00Z")

    def write(self, folder, name, cwd, stamp):
        path = self.root / folder / (name + ".jsonl")
        path.parent.mkdir(exist_ok=True)
        rows = [
            {
                "type": "attachment",
                "cwd": str(cwd),
                "gitBranch": "feature",
                "timestamp": stamp,
            },
            {"type": "custom-title", "customTitle": "Warmup work"},
            {
                "type": "user",
                "message": {"content": "Please preserve all my requirements."},
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "thinking", "thinking": "private reasoning"},
                        {
                            "type": "tool_use",
                            "id": "t1",
                            "name": "Bash",
                            "input": {"command": "test"},
                        },
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "t1",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "x" * 800 + "\nTEST FAILED\nneedle at end",
                                },
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "data": "SECRET_IMAGE_BYTES",
                                    },
                                },
                            ],
                        }
                    ]
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Edit",
                            "id": "t2",
                            "input": {
                                "file_path": "app.swift",
                                "old_string": "a",
                                "new_string": "b",
                            },
                        }
                    ]
                },
            },
        ]
        path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        return path

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--file", str(self.path), *args],
            text=True,
            capture_output=True,
            check=True,
        ).stdout

    def test_compact_preserves_dialogue_and_evidence(self):
        output = self.run_cli()
        self.assertIn("Please preserve all my requirements.", output)
        self.assertIn("TEST FAILED", output)
        self.assertIn("no result recorded", output)
        self.assertIn("L6 CALL Edit t2", output)
        self.assertIn("condensed", output)
        self.assertNotIn("SECRET_IMAGE_BYTES", output)
        self.assertNotIn("private reasoning", output)

    def test_expand_tool_and_lines(self):
        for args in [("--tool", "t1"), ("--lines", "4:5")]:
            output = self.run_cli(*args)
            self.assertIn("x" * 800, output)
            self.assertIn("L4 CALL Bash t1", output)
            self.assertIn("L5 RESULT t1", output)
            self.assertNotIn("SECRET_IMAGE_BYTES", output)
        self.assertIn("private reasoning", self.run_cli("--lines", "4", "--reasoning"))

    def test_search_finds_condensed_content(self):
        output = self.run_cli("--search", "needle")
        self.assertIn("needle at end", output)
        self.assertIn("L5 RESULT t1", output)
        self.assertNotIn("L4 CALL", output)

    def test_tail(self):
        output = self.run_cli("--tail", "1")
        self.assertIn("L6 CALL Edit t2", output)
        self.assertNotIn("L5 RESULT", output)

    def test_scoped_selection_and_explicit_id(self):
        other = self.write(
            "b", "session-b", self.root / "elsewhere", "2026-02-01T00:00:00Z"
        )
        args = type(
            "Args",
            (),
            dict(
                file=None,
                session=None,
                cwd=str(self.project),
                all_dirs=False,
                match=None,
                list=False,
            ),
        )()
        with patch.object(reader, "ROOT", self.root):
            self.assertEqual(reader.locate(args), self.path)
            args.match = "warmup"
            self.assertEqual(reader.locate(args), self.path)
            args.match = None
            args.all_dirs = True
            self.assertEqual(reader.locate(args), other)
            args.all_dirs = False
            args.cwd = str(self.root / "missing")
            with self.assertRaises(ValueError):
                reader.locate(args)
            args.session = "session-b"
            self.assertEqual(reader.locate(args), other)

    def test_malformed_line_warns_and_preserves_line_numbers(self):
        self.path.write_text(
            self.path.read_text()
            + "{broken\n"
            + json.dumps({"type": "user", "message": {"content": "last"}})
            + "\n"
        )
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            rows = list(reader.records(self.path))
        self.assertIn(":7:", errors.getvalue())
        self.assertEqual(rows[-1][0], 8)

    def test_invalid_range_and_tail(self):
        for args in [("--lines", "5:2"), ("--tail", "0")]:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), *args], capture_output=True
            )
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
