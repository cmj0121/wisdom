---
name: lsp
description: Checks whether a repo is large and typed enough for a language server to pay off, and names the official LSP plugin to enable. Use before heavy code work.
license: MIT
metadata:
  shortcut: "need lsp"
---

# LSP

Decide whether enabling a language server is worth it for this repo. A language server gives
the agent go-to-definition, find-references and post-edit diagnostics: fewer broad greps and
whole-file reads, and type errors caught before a build. It only pays off where there is
enough typed code to navigate. Report — never install a plugin, a binary or a setting.

## Steps

1. **Count source files** per language with `git ls-files`, so vendored and ignored files
   stay out. Map extensions with the table below; anything else is not a candidate.

   | Language | Extensions            | Plugin              | Binary                       |
   | -------- | --------------------- | ------------------- | ---------------------------- |
   | TS / JS  | `.ts .tsx .js .jsx`   | `typescript-lsp`    | `typescript-language-server` |
   | Python   | `.py .pyi`            | `pyright-lsp`       | `pyright-langserver`         |
   | Go       | `.go`                 | `gopls-lsp`         | `gopls`                      |
   | Rust     | `.rs`                 | `rust-analyzer-lsp` | `rust-analyzer`              |
   | C / C++  | `.c .h .cpp .cc .hpp` | `clangd-lsp`        | `clangd`                     |
   | C#       | `.cs`                 | `csharp-lsp`        | `csharp-ls`                  |
   | Java     | `.java`               | `jdtls-lsp`         | `jdtls`                      |
   | Kotlin   | `.kt .kts`            | `kotlin-lsp`        | `kotlin-lsp`                 |
   | Swift    | `.swift`              | `swift-lsp`         | `sourcekit-lsp`              |
   | Ruby     | `.rb .rake .erb`      | `ruby-lsp`          | `ruby-lsp`                   |
   | PHP      | `.php`                | `php-lsp`           | `intelephense`               |
   | Lua      | `.lua`                | `lua-lsp`           | `lua-language-server`        |

   Plugins come from the `claude-plugins-official` marketplace. If its catalogue is cached
   locally, check it for the current names before trusting this table.

2. **Judge each language.** Worth it when the language has **100 or more** files, or fewer
   but one package with deep cross-file calls (a monorepo of small files counts). Not worth
   it for a repo that is mostly Markdown, YAML or shell, or for a language under 20 files.
   The numbers are a rule of thumb; say so when a language sits near them.

3. **Check what is already on.** For each worth-it language:
   - **Plugin enabled:** `<plugin>@claude-plugins-official` is `true` under `enabledPlugins`
     in `~/.claude/settings.json`, `.claude/settings.json` or `.claude/settings.local.json`.
     An `LSP` tool in this session means at least one server is loaded.
   - **Binary installed:** `command -v <binary>`. The plugin does not ship it; without it
     the plugin loads and reports "Executable not found in $PATH" under `/plugin` → Errors.

## Output

One row per language that has any files, largest first:

| Language | Files | Worth it? | Plugin | Enabled | Binary |
| -------- | ----- | --------- | ------ | ------- | ------ |

Then, for each worth-it language not fully on, the missing steps only:

```text
/plugin install <plugin>@claude-plugins-official
```

and that `<binary>` must be installed on `PATH` with the language's own toolchain — see the
plugin's README. Restart the session after enabling so the server loads.

End with one sentence: enable LSP for which languages, or not needed and why.
