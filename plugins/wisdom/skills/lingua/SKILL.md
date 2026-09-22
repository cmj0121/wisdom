---
name: lingua
description: Answers in the user's chosen language whatever they write in, remembered per project. Use to set, change or show that preference; not for translating files.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
metadata:
  shortcut: "reply in"
---

# Lingua

Keep a per-project response-language preference and apply it. Output language only: it
never changes what is answered.

## Config

`~/.claude/projects/<project-path>/memory/lingua.md`, where `<project-path>` is the working
directory with `/` replaced by `-`. Never committed.

```yaml
---
respond_in: zh-TW # reply language; required
discuss_in: auto # the language the user writes in; auto = detect
refine_question: false # restate the question in one line before answering
keep_terms_in: en # code, identifiers and technical terms stay in this language
glossary: [] # term normalisations, e.g. "K8s → Kubernetes"
---
```

The plugin's SessionStart hook loads this file into every new session, so a saved
preference needs no magic word afterwards.

## Steps

1. **Load** the config. Present: apply it (below). Missing: ask the user — reply language,
   whether to restate questions, whether to keep technical terms untranslated — then write
   the file and confirm in one line. Never guess a language from the one the user writes in.
2. **Apply** for the rest of the session:
   - write every reply in `respond_in`;
   - keep code, identifiers, commands, paths and technical terms verbatim in
     `keep_terms_in`, applying `glossary`;
   - with `refine_question: true`, open with a one-line restatement of the question in
     correct terminology — skip it when the question is already precise.
3. **Change** on request ("reply in Japanese", "stop restating"): edit the file, confirm in
   one line, apply at once. `lingua off` pauses the rules for this session without touching
   the file.
4. **Show** when invoked with nothing to change: the active settings and the file path.
