# Git Committer Plugin

> Assists in creating clear and concise git commit messages following conventional commit format.

The git-committer plugin helps you write well-structured git commit messages. It reads your
project's commit template (if configured), reviews staged changes, drafts a conventional commit
message, and confirms with you before committing.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install git-committer
```

## How It Works

### Commit Workflow

1. **Template detection** - Checks `git.commit.template` config for a custom format
2. **Stage changes** - Reviews working tree and stages relevant files
3. **Review diffs** - Reads staged diffs to understand the changes
4. **Draft message** - Writes a commit message in conventional commit format
5. **User confirmation** - Presents the draft and waits for approval before committing

### Conventional Commit Format

```txt
<type>(scope): <Short description>

    <body>

    <footer>

    Committer: <model name>
```

Supported types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and more.

## Usage

### Slash Command

```text
/commit
```

Triggers the full commit workflow directly.

### Magic Word

Typing a prompt that contains `commit` will auto-dispatch this skill via the shortcut plugin.

## License

MIT
