# /commit-it

A streamlined git-flow-only path that skips planning and implementation, going straight to
review, commit, and session summary.

## Instructions

1. **Review** -- Invoke `code-reviewer:review` (code-reviewer) on the current changeset.
   Use `git diff` and `git diff --staged` to identify the scope of changes.

2. **Evaluate findings** -- Inspect the review results:

   - If **Critical** findings exist, present them to the user and ask whether to fix or
     abort. Do not proceed to commit until the user decides.
   - If only **Warnings** or **Suggestions** exist, present them briefly and proceed to
     commit.

3. **Commit** -- Invoke `git-committer:commit` (git-committer) to handle staging, message drafting,
   and user confirmation. The git-committer will skip its own review step since we already
   reviewed above.

4. **Session result** -- Emit the summary table and machine-readable result block:

   ```text
   __SESSION_RESULT__
   steps_planned: 2
   steps_completed: <count>
   review_cycles: <count>
   final_verdict: PASS | WARN | FAIL
   commit_hash: <short hash or none>
   tests_passed: skipped
   status: COMPLETE | PARTIAL | ABORTED
   __SESSION_RESULT__
   ```

   - `steps_planned` is always `2` (review + commit).
   - `steps_completed` is `2` if both review and commit succeeded, `1` if only review
     ran, `0` if aborted before review.
   - `final_verdict` is `PASS` if committed with no Critical or Warning findings, `WARN`
     if committed with Warnings, `FAIL` if aborted due to Critical findings.
   - `tests_passed` is `skipped` since this workflow does not run tests.
