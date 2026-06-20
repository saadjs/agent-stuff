---
name: scratch-log
description: Keep a running log of decisions, tradeoffs, assumptions, review fixes, and open questions during multi-step work, so the user can read back what was chosen and what they never specified. Use on any non-trivial task, and when invoked as /scratch-log.
---

Log the reasoning *around* the code that the diff won't show, so the user can later audit two things: tradeoffs you made (and why), and what they forgot to specify.

File: `.scratch/<branch-or-task>.md`, one per branch/task. Ensure `.scratch/` is gitignored; never commit unless asked.

Append as you go, while reasoning is fresh, not in one batch at the end. Terse, scannable, grouped by section. Capture:

- **Assumptions / unspecified** — what the user didn't say that you had to fill in. Tag `[needs review]`. This is what they're scanning for; keep it distinct.
- **Decisions & tradeoffs** — choice, rejected alternative, why.
- **Review fixes** — issue found, how resolved.
- **Open questions / TODOs** — unresolved/deferred, tag `[ ]`.
- Anything else the diff won't make obvious (dead ends, surprising constraints, intentional-but-looks-wrong).

Skip what the diff/commits already say. Skip the log entirely on trivial fully-specified one-steps.

On finishing a chunk, point at the file, don't dump it: "Logged assumptions + tradeoffs in `.scratch/<branch>.md`, a couple are guesses worth correcting." Name the riskiest guess.
