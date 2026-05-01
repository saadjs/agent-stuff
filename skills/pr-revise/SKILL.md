---
name: pr-revise
description: Address GitHub Pull Request feedback with the gh CLI. Use when a user provides a PR number and asks to fetch comments, verify which comments are meaningful, add regression tests, implement fixes, run all tests, and push the branch.
---

# GH Address PR Comments

## Goal

Resolve actionable PR feedback end-to-end with evidence:

1. Fetch all PR comments with `gh`.
2. Prove meaningful comments with failing regression tests.
3. Apply minimal fixes.
4. Run the full test suite.
5. Commit and push updates.
6. Post reply comments describing what was fixed.
7. Re-request review from the original reviewer(s).

## Preconditions

Verify GitHub auth, ensure a clean working tree, then check out the PR branch with `gh pr checkout`.

## Workflow

1. Fetch PR comments — review summaries, inline code comments, and issue-level comments via `gh pr view` and `gh api`.

2. Build a comment checklist. For each comment record: author, location, requested change, and classification (`meaningful` or `not-meaningful`). Classify as `meaningful` only when the comment identifies a verifiable defect, regression risk, missing test, or concrete requirement mismatch.

3. Add regression tests before code fixes for meaningful comments. Each meaningful comment should map to a failing test. If no failing test can be produced, either downgrade the comment to `not-meaningful` or explicitly record why it's non-testable.

4. Implement minimal fixes tied to checklist items. Avoid unrelated refactors. Re-run narrow tests after each fix.

5. Run the full test suite. Do not continue to commit/push with failing tests.

6. Commit and push. Review diff for comment-to-change traceability. Commit with focused messages, then push.

7. Post GitHub reply comments after push. For each meaningful addressed comment, reply on the same thread. Reply body: what changed, commit SHA(s), and test evidence when applicable.

8. Re-request review from original reviewers via `gh pr edit --add-reviewer` or comment-driven triggers (e.g., `@codex review`).

9. Report: meaningful comments addressed, non-meaningful rejections with rationale, tests added, test result, pushed branch, reply comments posted, re-review requested.

## Guardrails

- Do not apply comment requests blindly.
- Do not mark a meaningful code comment resolved without a regression test or an explicit reason it's non-testable.
- Do not push if the full suite fails.
