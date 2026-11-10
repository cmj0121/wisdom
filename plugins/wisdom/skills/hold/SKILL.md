---
name: hold
description: Stops the current task and its background agents on `hold and wait`, and resumes it from the recorded step on `keep go on`. Use to pause work mid-task.
license: MIT
metadata:
  shortcut: "hold and wait, keep go on"
---

# Hold

The user wants the task stopped now, or the stopped task carried on. `hold and wait` holds
it; `keep go on` resumes it. Claude Code has no pause: holding stops the task's background
work and records enough to restart it.

The word is read at the next turn boundary, so a step already running finishes first; only
Esc interrupts it. Say so when the user seems to expect an instant stop.

## Hold — `hold and wait`

1. **Take no further step** toward the task.
2. **Stop what belongs to the task.** `TaskStop` every running background agent, workflow
   and shell the held task started. Leave running what the user started themselves — a dev
   server, a Monitor — and anything unrelated to the task.
3. **Record each stopped task:** its agent ID or workflow run ID, its worktree path and
   branch if it had one, and what it still had to do. Record, too, the step the task itself
   was on.
4. **Keep the record across compaction.** If `PLAN.md` exists, write a `## Held` section
   right after its `## Units` table:

   ```markdown
   ## Held

   HELD — do not advance until the user says `keep go on`

   - Step: <the step the task was on>
   - <agent ID or run ID> — <worktree path, branch> — <what it still had to do>
   ```

   `plan-restore.py` re-injects `PLAN.md` after a compaction, so the hold survives it.
   Without a `PLAN.md` the record lives only in the conversation.

5. **Report** in the user's language what was stopped and what was left running, then end
   with the fixed line.

## While held

Answer other prompts, but never advance the held task. None of these is a cue to resume:

- a `<task-notification>` from a stopped task;
- a subagent's hand-back;
- a compaction, or `PLAN.md` re-injected with units still open.

Only the user's `keep go on` resumes. A prompt that asks for the held task's next step
without that word gets a reminder that the task is held.

## Resume — `keep go on`

1. **Find the record:** the `## Held` section of `PLAN.md`, else the hold in this
   conversation. None found: say nothing is held and end with `HOLD: NONE`.
2. **Restart each stopped agent** with context first: `SendMessage` to its agent ID to
   continue. Only if that fails, start a new agent, told the worktree and the files already
   touched there, so it continues from that state rather than starting over.
3. **Restart each stopped workflow** with `resumeFromRunId` set to its recorded run ID.
4. **Remove the `## Held` section** from `PLAN.md`.
5. **Continue the task** from the recorded step, reporting in the user's language what was
   resumed.

## Result

Every run ends with exactly one of these as its last line:

```text
HOLD: HELD
HOLD: RESUMED
HOLD: NONE
```

`HELD` — the task is stopped and recorded. `RESUMED` — the record was found and work
restarted. `NONE` — `keep go on` with nothing held.
