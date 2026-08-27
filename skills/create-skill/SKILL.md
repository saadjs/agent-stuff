---
name: create-skill
description: Create a small, reliable agent skill without prompt bloat.
disable-model-invocation: true
---

# Create skill

1. Define one job, defaults, opt-ins, done state. Inspect existing skills.

2. Choose invocation:
   - Human runs it: `disable-model-invocation: true`; one-line human description.
   - Agent must discover it: omit flag; description names each real trigger branch.

3. Use only needed parts:

```text
<skill>/
├── SKILL.md     # required: metadata + instructions
├── scripts/     # optional: executable code
├── references/  # optional: on-demand docs
└── assets/      # optional: templates/resources
```

4. Write ordered actions. Each: command/decision + checkable bound. Inspect before edits; preserve user work; verify after.

5. Keep common path in `SKILL.md`. Move opt-ins/reference to short linked files. Link upstream instructions when freshness matters; avoid copies likely to drift.

6. Prune hard:
   - one meaning, one place
   - commands over exposition
   - positive target over prohibitions
   - no synonyms, motivation, generic advice, or restated environment
   - fragments welcome
   - start under 200 words; add only to prevent observed ambiguity

7. Add scripts/assets only when needed. Preserve files; fail clearly; support reruns.

8. Validate frontmatter, links, commands, script smoke tests, `git diff --check`. Re-read once; delete every sentence that does not change agent behavior.

Done: smallest reliable process; branches explicit; checks pass.
