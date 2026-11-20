"""Recognises a wisdom:plan PLAN.md, shared by the hooks that restore or save it."""


def cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_plan(content: str) -> bool:
    """True when a `## Units` heading is followed by a table with a `Status`
    column and at least one data row."""
    lines = content.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "## Units")
    except StopIteration:
        return False

    table = []
    for line in lines[start + 1:]:
        if line.strip().startswith("|"):
            table.append(line)
        elif table or line.startswith("#") or line.strip():
            break
    return len(table) >= 3 and "Status" in cells(table[0])
