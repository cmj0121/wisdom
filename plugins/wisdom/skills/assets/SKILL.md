---
name: assets
description: Builds image, video or audio assets one confirmed change per round against locked concepts. Use when a media asset must converge instead of drifting.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
metadata:
  shortcut: "build assets"
---

# Assets

Build a media asset — image, video, audio — in rounds. Each round changes one thing against
a fixed base, so the asset converges instead of drifting. The skill owns the loop and the
lock files; generating belongs to whatever backend the environment already has.

This version is written against images. Video and audio run the same loop as far as the
backend allows; there are no timeline, clip or track fields.

## Inputs

Ask for the missing ones in a single question; never pick one.

- **Session directory** (`$SESSION`) — where the lock files and candidates live. The caller
  decides it before this skill runs: a project or a session directory, in git or not.
- **Set and asset** — the set names the lock file (`<set>_assets.lock`); the asset names
  the entry in it.
- **Shared concepts** — on a first run with no global lock, which concepts every asset
  shares; none is an answer.
- **Language** — the `lingua` preference in context, else the user's language. The round
  spec's labels are written in it too.

## Lock files

YAML, hand-editable, and only confirmed state — a candidate never enters a lock.

`$SESSION/ASSETS.global.lock` — concepts every asset in the project shares:

```yaml
concepts:
  style: hand-drawn watercolour, low saturation
  character: a stuffed bear with a notched left ear
```

`$SESSION/<set>_assets.lock` — one asset set:

```yaml
candidates: 3 # the count last confirmed for this set
assets:
  bear:
    current: candidates/bear-r1-2.jpg # the last pick: the next round's base
    frozen: [face, pose, crop, background]
    local: # confirmed concepts of this asset alone
      belly: short hemp threads round the tear
    history:
      - base: images/38.jpg
        change: add a ring of short hemp threads round the belly tear
        scope: the edge of the tear only
        picked: candidates/bear-r1-2.jpg
```

Global, `frozen` and `local` concepts all constrain a round, except the one concept the
round changes. A local concept may add to the global ones, never override one: a change
that contradicts a global concept stops the round — ask whether the global concept itself
is to change, since that reaches every asset. On a yes the change is written with the pick
to the global lock, not under `local`.

## Round

1. **Load** both lock files when they exist. Neither existing is a first run, not an error.
2. **Base.** The asset's `current`; with no entry, the file the user names. With no base at
   all, design one first: a round whose spec has no base and whose change is the asset's
   description.
3. **Frozen and change.** Frozen defaults to the lock's `frozen`. The change comes from the
   user, one per round — two changes are two rounds; ask which goes first.
4. **Scope.** The region or aspect the change may touch. Given the change but no scope,
   propose the smallest scope that can hold it rather than asking an open question.
5. **Candidates.** The count the user last gave, else the lock's `candidates`, else 3.
6. **Confirm.** Show the round spec and stop — the only confirmation stop in a round.
   Generate nothing before the user confirms; an edited line is applied and the spec shown
   again. In English the labels are `Base`, `Frozen`, `Change`, `Scope`, `Candidates`.

   ```text
   基準: images/38.jpg
   凍結: 臉、姿勢、剪裁、背景
   改: 腹部破口邊緣加一圈短麻線
   範圍: 只動破口邊緣
   候選: 3
   ```

7. **Generate** with the image, video or audio tool available in the session (an MCP
   server or a CLI). The prompt carries the base, every constraining concept, the change
   and the scope. Save the candidates as `$SESSION/candidates/<asset>-r<round>-<n>.<ext>`,
   `<round>` being one past the highest already on disk for the asset, and show their
   paths. With no such tool, output the spec and the prompt, say that nothing was
   generated, and wait for the user's files.
8. **Pick.** On a pick, write the asset's entry to `<set>_assets.lock`, creating both lock
   files on the first pick, the global one even with no concepts: set `current` to the
   pick, record the change under `local`, keep the confirmed `frozen`, append the round to
   `history`, store the candidate count. Shared concepts go to `ASSETS.global.lock`. No
   pick writes nothing, and the next round keeps the same base.

Never delete a candidate: the unpicked ones are the user's to clean up.
