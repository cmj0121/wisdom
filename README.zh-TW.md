# Wisdom

> 讓你的 Claude Code 像我一樣，做事更有效率、更有成效

[English](README.md)

Wisdom 是我每天在用的 Claude Code skill 合集，打包成單一 plugin，讓你能照我的方式使用。

## 安裝

```bash
/plugin marketplace add cmj0121/wisdom
/plugin install wisdom@wisdom
```

## 核心概念

v3 從零重寫，圍繞三條規則。

1. **一個 skill，一個目的。** 每個 skill 只做一件事，並以該件事命名。需要第二項工作時，
   呼叫負責那件事的 skill，而不是自己長出新職責。
2. **需要時才用 shortcut。** 每個 skill 都能以 `/wisdom:<name>` 執行。常用到會順口說出的
   skill 另外宣告 magic word——例如說 `smith`，dispatcher 就會啟動主導 skill。magic word 在
   整個 plugin 內不得重複。
3. **更少的 token。** `description` 每個 session 都會載入，所以只寫一句短句；body 在每次
   執行時載入，同樣保持精簡；只有部分執行才需要的內容放在 `references/`，需要時才讀。不設
   人設、不做角色扮演、不重複探索專案：由計畫檔把 context 往下傳遞。

## Skills

`smith` 是入口。告訴它你要做什麼，它會先規劃，再依序呼叫其他 skill。每個 skill 也都能單獨使用。

### 主導

| Skill   | 目的                                      | Magic word |
| ------- | ----------------------------------------- | ---------- |
| `smith` | 以下列 skill 把一項工作從想法推進到 merge | `smith`    |

### 建構

| Skill    | 目的                                       | Magic word    |
| -------- | ------------------------------------------ | ------------- |
| `plan`   | 把想法寫成 `PLAN.md`：目標、工作單元、決策 | `plan it`     |
| `design` | 決定架構、API 或技術選型，並列出取捨       | `design it`   |
| `spec`   | 為已定案的設計撰寫技術規格                 | `write spec`  |
| `code`   | 實作一個工作單元及其測試                   | `code it`     |
| `test`   | 執行專案的測試套件並回報結果               | `run tests`   |
| `review` | 審查一份 diff 的正確性與品質               | `review it`   |
| `docs`   | 撰寫或更新面向使用者的文件                 | `document it` |

### 交付

| Skill       | 目的                                        | Magic word      |
| ----------- | ------------------------------------------- | --------------- |
| `commit`    | 為已 stage 的變更撰寫 commit message 並提交 | `commit it`     |
| `changelog` | 從 git 歷史產生 changelog 條目              | `gen changelog` |
| `release`   | 升版並打 tag 發佈——只在你要求時執行         | `release it`    |
| `resolve`   | 以測試先行的方式處理 PR 的 review 意見      | `resolve pr`    |

### 檢查

| Skill       | 目的                             | Magic word   |
| ----------- | -------------------------------- | ------------ |
| `secure`    | 審查原始碼的安全問題，對應到 CWE | `sec review` |
| `audit`     | 稽核相依套件的已知漏洞與過期版本 | `audit deps` |
| `ops`       | 發佈前審查維運就緒程度           | `ops review` |
| `challenge` | 反對一項計畫，點出其盲點         | `tenth man`  |
| `lsp`       | 判斷專案是否需要 language server | `need lsp`   |

### 輸出

| Skill      | 目的                                         | Magic word       |
| ---------- | -------------------------------------------- | ---------------- |
| `diagram`  | 為已定案的結構畫 ASCII 圖                    | `draw a diagram` |
| `compact`  | 把上一個回答重新整理成精簡表格               | `compact it`     |
| `brief`    | 讓回答保持簡短，一次只討論一個主題           | `brief me`       |
| `lingua`   | 以你選定的語言回答，並依專案記住             | `reply in`       |
| `shortcut` | 依 prompt 中出現的 magic word 派送對應 skill | —                |

## smith 如何運作

```text
  idea ──> smith ──> plan ──> (design) ──> code ×N ──> review ──> docs ──> commit
             │         │                     ▲           │
             │         └── challenge         └── fix ────┘
             │
             └── release · only when you ask
```

- `plan` 只寫一次 `PLAN.md`——context、工作單元、決策——之後每個 skill 都讀它，不再重新探索專案。
- 互相獨立的工作單元平行執行，每個 `code` 各自在獨立的 git worktree 中。
- `review` 回傳一行 verdict；失敗時 `smith` 把它送回 `code`（設計有問題時則送回 `design`）。
- `smith` 只會停下來問你兩次：核准計畫、核准 merge。除非你要求，它不會打 tag 或發佈。

## Token 預算

| 部分              | 何時載入     | 預算                         |
| ----------------- | ------------ | ---------------------------- |
| `description`     | 每個 session | 一句話，≤ 160 字元           |
| `SKILL.md` body   | 每次執行     | ≤ 100 行（`smith` ≤ 150 行） |
| `references/*.md` | 僅在需要時   | 不設限，一個檔案一個主題     |

## 開發

Skill 是帶有 YAML frontmatter 的 Markdown，遵循
[Agent Skills standard](https://agentskills.io/specification)；沒有 build 步驟。

```text
plugins/wisdom/
├── .claude-plugin/plugin.json
├── hooks/               # hooks.json 與它執行的腳本
└── skills/<name>/
    ├── SKILL.md
    └── references/      # optional
```

commit 前請執行 `make test`——它會檢查目錄結構、版本同步、frontmatter 是否符合標準，以及
magic word 是否重複。

## DDD（Dream-Driven Development）

本專案遵循 DDD（Dream-Driven Development，夢想驅動開發）：由我所想像的願景驅動。所有功能
都來自我自己的需求與夢想。
