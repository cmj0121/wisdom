---
name: afk
description: Keeps the agent working to the end and pings the terminal only when it is done or needs the user. Use when the user steps away from a long task.
license: MIT
metadata:
  shortcut: "afk mode"
---

# Afk

The user is away from the keyboard. Apply these rules for the rest of the session: work to
the end, and stop only when the terminal should call the user back. They change when you
stop, never what you may do: the mode widens no permission and skips no confirmation the
user would otherwise get.

## Turn on

Run the switch with Bash, by its path from this skill's base directory (printed when the
skill loads):

```bash
python3 "<base directory>/../../hooks/afk-notify.py" on
```

Read what it prints, not its exit code. `afk: on` means the notifications are armed;
anything else means the mode did not turn on — tell the user what it printed, and that they
will get no ping.

## Rules

1. **Work to the end.** Carry the task through to completion. No progress check-ins, no
   "shall I continue?", no stopping to report a finished step.
2. **Decide the ordinary yourself.** An obstacle with a reasonable way round, or a choice
   that is easy to reverse, is yours to make. Note each decision and its reason, and list
   them in the final report.
3. **Stop for three things only:** the task is complete; a question only the user can
   answer; or the next action is hard to undo or faces outward (a push, a release, a
   deletion, a message sent in the user's name) and the user has not asked for it in this
   conversation. One they did ask for is carried out, and any permission prompt it raises
   still reaches them.
4. **Ask in plain text.** End the turn with the question written in the message, not
   through a dialog tool — the hook carries the message's last line into the notification.
5. **End every turn with one fixed line.** The last line of any message that ends a turn is
   exactly one of:

   ```text
   AFK: DONE
   AFK: ASK — <the question, on one line>
   ```

   Nothing follows it. Without the line the user is pinged with a bare "stopped" and cannot
   tell which it was.

## Stop

`afk off` ends the mode for the rest of the session: run the same script with `off`, expect
`afk: off`, and drop the fixed line. An answer to an `AFK: ASK` is not a request to stop —
keep working under the rules.
