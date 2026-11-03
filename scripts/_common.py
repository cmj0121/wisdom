"""Helpers shared by the check scripts. Each wrapper puts scripts/ on PYTHONPATH."""
import glob
import os
import re

GREEN, RED, RESET = "\033[32m", "\033[31m", "\033[0m"
# Quiet by default; WISDOM_VERBOSE=1 restores the per-item PASS lines. See
# scripts/test for why an environment variable, and why not a bare VERBOSE.
WISDOM_VERBOSE = os.environ.get("WISDOM_VERBOSE", "") not in ("", "0")
_errors = 0


def ok(msg):
    if WISDOM_VERBOSE:
        print(f"  {GREEN}PASS{RESET} {msg}")


def bad(msg):
    global _errors
    print(f"  {RED}FAIL{RESET} {msg}")
    _errors += 1


def error_count():
    return _errors


def source_path(entry):
    """A marketplace.json plugin entry's source, relative to the repo root."""
    source = entry["source"]
    return source[2:] if source.startswith("./") else source


def skill_files(root, source="plugins/*"):
    """Sorted SKILL.md paths under one plugin source, by default under every plugin."""
    return sorted(glob.glob(os.path.join(root, source, "skills", "*", "SKILL.md")))


def shipped_skills(root, plugins):
    """Yield (skill, SKILL.md path) for each marketplace.json plugin entry."""
    for entry in plugins:
        for path in skill_files(root, source_path(entry)):
            yield os.path.basename(os.path.dirname(path)), path


# ------------------------------------------------------------ the YAML subset
#
# Not a YAML parser: just enough of one to read the frontmatter shapes this
# repo uses, so the checks have no dependency the repo does not already have.
# Anything it cannot read is reported rather than skipped.


def split_frontmatter(path):
    """Return (frontmatter_lines, body_lines), or (None, None) if unterminated."""
    lines = open(path, encoding="utf-8").read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1 :]
    return None, None


def parse_frontmatter(lines):
    """Map top-level keys to a str, a dict, or a list.

    Handles the three shapes present here: a scalar, a folded block ('>-',
    whose lines rejoin with a single space), and an indented block that is
    either a mapping or a sequence.
    """
    fields, i = {}, 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        block, i = [], i + 1
        while i < len(lines) and (not lines[i].strip() or lines[i].startswith(" ")):
            block.append(lines[i])
            i += 1
        while block and not block[-1].strip():
            block.pop()

        if rest in (">-", ">", "|", "|-"):
            joiner = "\n" if rest.startswith("|") else " "
            fields[key] = joiner.join(b.strip() for b in block)
        elif rest:
            fields[key] = rest.strip("'\"")
        elif block and block[0].lstrip().startswith("- "):
            fields[key] = [b.strip()[2:].strip() for b in block]
        elif block:
            sub = {}
            for b in block:
                sm = re.match(r"^\s+([A-Za-z0-9_-]+):(.*)$", b)
                if sm:
                    sub[sm.group(1)] = sm.group(2).strip().strip("'\"")
                else:
                    sub[b.strip()] = None  # unreadable -> reported by the check
            fields[key] = sub
        else:
            fields[key] = ""
    return fields
