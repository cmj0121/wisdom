"""Rebuild a branch from a classification manifest; see ../SKILL.md for its shape.

The checkout is touched once, by the final soft reset, after the rebuilt tree is
proven equal. Every exit removes the worktree and prints a HISTORY: line last.
"""
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

FOOTER = re.compile(r"^(Refs|Closes)[: ]")
TRAILER = re.compile(r"^[\w-]+(:\s| #)")
KINDS = {"bump", "docs", "purpose", "fix", "test"}
NEW_DOCS = "docs: update documentation"
NEW_TEST = "test: add tests"


class Stop(Exception):
    """End the run with this outcome; `detail` is printed above the HISTORY: line."""

    def __init__(self, outcome, reason, detail=""):
        super().__init__(reason)
        self.outcome, self.reason, self.detail = outcome, reason, detail


class Step:
    """One commit to build: what to take, whose message, and footers it inherits."""

    def __init__(self, source, takes, message=None):
        self.source, self.takes, self.message = source, takes, message
        self.footers = []


def raw(cwd, *args):
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        errors="surrogateescape",
    )


def output(done):
    """Everything a failed command said; hooks write to either stream."""
    return done.stdout + done.stderr


def git(cwd, *args):
    done = raw(cwd, *args)
    if done.returncode:
        subcommand = next(a for a in args if not a.startswith("-"))
        raise Stop("ABORTED", f"git {subcommand} failed", output(done))
    return done.stdout


def footers_of(cwd, rev_range):
    return [line for line in git(cwd, "log", "--format=%B", rev_range).splitlines() if FOOTER.match(line)]


def paths_of(cwd, sha):
    out = git(cwd, "diff-tree", "--no-commit-id", "--name-only", "-z", "-r", "--no-renames", sha)
    return [p for p in out.split("\0") if p]


def take(wt, rev, paths):
    for path in paths:
        if raw(wt, "cat-file", "-e", f"{rev}:{path}").returncode == 0:
            git(wt, "--literal-pathspecs", "checkout", "-q", rev, "--", path)
        else:
            git(wt, "--literal-pathspecs", "rm", "-qf", "--ignore-unmatch", "--", path)


def with_footers(message, footers):
    lines = message.rstrip("\n").split("\n")
    new = [f for f in dict.fromkeys(footers) if f not in lines]
    if not new:
        return message
    last_block = message.rstrip("\n").split("\n\n")[-1].split("\n")
    in_block = len(message.rstrip("\n").split("\n\n")) > 1 and all(TRAILER.match(l) for l in last_block)
    return "\n".join(lines + ([] if in_block else [""]) + new) + "\n"


def commit(wt, step):
    """Commit what is staged, keeping the source's author and date; the raw result."""
    if not step.footers and step.message is None:
        return raw(wt, "commit", "-q", "-C", step.source)
    message = step.message or git(wt, "log", "-1", "--format=%B", step.source)
    author = git(wt, "log", "-1", "--format=%an <%ae>", step.source).strip()
    date = git(wt, "log", "-1", "--format=%aI", step.source).strip()
    return commit_message(wt, with_footers(message, step.footers), f"--author={author}", f"--date={date}")


def commit_message(wt, message, *flags):
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, "w", encoding="utf-8", errors="surrogateescape") as handle:
            handle.write(message)
        return raw(wt, "commit", "-q", "-F", path, *flags)
    finally:
        os.unlink(path)


def staged(wt):
    return [p for p in git(wt, "diff", "--cached", "--name-only", "-z").split("\0") if p]


def check_manifest(manifest):
    kinds = {c["sha"]: c["kind"] for c in manifest["commits"]}
    for entry in manifest["commits"]:
        if entry["kind"] not in KINDS:
            raise Stop("ABORTED", f"unknown kind {entry['kind']} for {entry['sha'][:8]}")
        target = entry.get("fold_into")
        if target and (entry["kind"] != "fix" or kinds.get(target) != "purpose"):
            raise Stop("ABORTED", f"{entry['sha'][:8]} cannot fold into {target[:8]}")


def preflight(top, manifest):
    """Return (start, mb, shas), or stop before any worktree exists."""
    base = manifest["base"]
    if raw(top, "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}").returncode:
        raise Stop("ABORTED", f"base ref {base} not found")
    if raw(top, "symbolic-ref", "-q", "HEAD").returncode:
        raise Stop("ABORTED", "HEAD is detached")
    if git(top, "status", "--porcelain", "--untracked-files=no").strip():
        raise Stop("ABORTED", "tracked changes in the checkout")
    count = git(top, "rev-list", "--count", f"{base}..HEAD").strip()
    if count == "0":
        raise Stop("UNCHANGED", f"no commits ahead of {base}")
    if count != git(top, "rev-list", "--count", f"{base}..HEAD", "--not", "--remotes").strip():
        raise Stop("UNCHANGED", "a commit is already on a remote")
    start = git(top, "rev-parse", "HEAD").strip()
    if manifest["start"] != start:
        raise Stop("ABORTED", "manifest start is not HEAD")
    mb = git(top, "merge-base", base, "HEAD").strip()
    shas = git(top, "rev-list", "--reverse", "--topo-order", "--no-merges", f"{mb}..{start}").split()
    if sorted(c["sha"] for c in manifest["commits"]) != sorted(shas):
        raise Stop("ABORTED", "manifest commits differ from the branch")
    if len(shas) <= 1:
        raise Stop("UNCHANGED", "one commit, nothing to reorder")
    return start, mb, shas


def plan(top, manifest, start, mb, shas):
    """Lay out every step, so a commit that disappears can hand its footers on."""
    by_sha = {c["sha"]: c for c in manifest["commits"]}
    docs, tests = list(manifest["docs"]), list(manifest["tests"])
    paths = {s: paths_of(top, s) for s in shas}
    code = {s: [p for p in paths[s] if p not in docs and p not in tests] for s in shas}
    kind = {s: by_sha[s]["kind"] for s in shas}
    fold = {s: by_sha[s].get("fold_into") for s in shas}
    # Footers of commits with no holder, and of merges, go to the last commit built.
    orphans = []
    for merge in git(top, "rev-list", "--merges", f"{mb}..{start}").split():
        orphans += footers_of(top, f"{merge}^!")

    bumps = [Step(s, [(s, paths[s])]) for s in shas if kind[s] == "bump"]

    doc_steps = [Step(s, [(s, [p for p in paths[s] if p in docs])]) for s in shas if kind[s] == "docs"]
    if docs and not doc_steps:
        doc_steps = [Step(start, [], NEW_DOCS)]
    if docs:
        doc_steps[-1].takes.append((start, docs))

    purposes = {s: Step(s, [(s, code[s])]) for s in shas if kind[s] == "purpose" and code[s]}
    folded = [s for s in shas if kind[s] == "fix" and fold[s]]
    for s in folded:
        if fold[s] not in purposes:
            raise Stop("ABORTED", f"{s[:8]} folds into a commit with no code paths")
        purposes[fold[s]].takes.append((s, code[s]))
        purposes[fold[s]].footers += footers_of(top, f"{s}^!")

    left, moved_to = [], {}
    for index, s in enumerate(shas):
        if kind[s] != "fix" or fold[s] or not code[s]:
            continue
        later = {}
        for other in shas[index + 1 :]:
            holder = purposes.get(other) if kind[other] == "purpose" else purposes.get(fold[other])
            if holder:
                for path in code[other]:
                    later.setdefault(path, holder)
        kept = [p for p in code[s] if p not in later]
        if kept:
            left.append(Step(s, [(s, kept)]))
        else:
            moved_to[s] = later[code[s][0]]

    test_step = None
    test_commits = [s for s in shas if kind[s] == "test"]
    if tests:
        holders = [s for s in test_commits if set(tests) <= set(paths[s])]
        if holders:
            test_step = Step(holders[-1], [(start, tests)])
        else:
            test_step = Step(test_commits[-1] if test_commits else start, [(start, tests)], NEW_TEST)

    # Every commit that built no step of its own hands its footers to whoever holds its paths.
    every = bumps + doc_steps + list(purposes.values()) + left + ([test_step] if test_step else [])
    kept = {step.source for step in every if step.message is None} | set(folded)
    for s in shas:
        if s in kept:
            continue
        footers = footers_of(top, f"{s}^!")
        if s in moved_to:
            moved_to[s].footers += footers
        elif doc_steps and set(paths[s]) & set(docs):
            doc_steps[-1].footers += footers
        elif test_step and set(paths[s]) & set(tests):
            test_step.footers += footers
        else:
            orphans += footers
    return bumps, doc_steps, [purposes[s] for s in shas if s in purposes], left, test_step, orphans


def own_footers(wt, step):
    return [] if step.message else footers_of(wt, f"{step.source}^!")


def build_docs(wt, doc_steps, last_purpose, start, orphans):
    """Build the docs commits, moving a rejected doc whole into the last purpose, once."""
    moved = set()
    for step in doc_steps:
        for rev, paths in step.takes:
            take(wt, rev, [p for p in paths if p not in moved])
        result = commit(wt, step) if staged(wt) else None
        if result is not None and result.returncode:
            if moved or last_purpose is None:
                raise Stop("ABORTED", f"hook rejected the docs commit of {step.source[:8]}", output(result))
            names = staged(wt)
            rejected = [p for p in names if p in output(result)] or names
            moved.update(rejected)
            take(wt, "HEAD", rejected)
            last_purpose.takes.append((start, rejected))
            result = commit(wt, step) if staged(wt) else None
            if result is not None and result.returncode:
                raise Stop("ABORTED", f"hook rejected the docs retry of {step.source[:8]}", output(result))
        if result is None:
            gone = step.footers + own_footers(wt, step)
            step_paths = {p for _, paths in step.takes for p in paths}
            if last_purpose is not None and step_paths & moved:
                last_purpose.footers += gone
            else:
                orphans += gone


def build(wt, bumps, doc_steps, purposes, left, test_step, orphans, start, mb):
    def plain(step):
        for rev, paths in step.takes:
            take(wt, rev, paths)
        if not staged(wt):
            orphans.extend(step.footers + own_footers(wt, step))
            return
        result = commit(wt, step)
        if result.returncode:
            raise Stop("ABORTED", f"hook rejected the commit of {step.source[:8]}", output(result))

    for step in bumps:
        plain(step)
    build_docs(wt, doc_steps, purposes[-1] if purposes else None, start, orphans)
    for step in purposes + left + ([test_step] if test_step else []):
        plain(step)
    if orphans and git(wt, "rev-parse", "HEAD").strip() != mb:
        message = git(wt, "log", "-1", "--format=%B", "HEAD")
        updated = with_footers(message, orphans)
        if updated != message:
            result = commit_message(wt, updated, "--amend")
            if result.returncode:
                raise Stop("ABORTED", "hook rejected the footer amend", output(result))


def verify(top, branch, start, mb, new):
    """Prove the rebuild equal, then move the branch. Returns the outcome and log."""
    if raw(top, "diff", "--quiet", start, new).returncode:
        raise Stop("ABORTED", "the rebuilt tree differs from start")
    if set(footers_of(top, f"{mb}..{start}")) != set(footers_of(top, f"{mb}..{new}")):
        raise Stop("ABORTED", "the Refs/Closes footers differ")
    if git(top, "log", "--format=%T", f"{mb}..{start}") == git(top, "log", "--format=%T", f"{mb}..{new}"):
        raise Stop("UNCHANGED", "already shaped")
    count = git(top, "rev-list", "--count", f"{mb}..{new}").strip()
    log = git(top, "log", "--oneline", f"{mb}..{new}")
    if git(top, "rev-parse", "HEAD").strip() != start or git(top, "symbolic-ref", "HEAD").strip() != branch:
        raise Stop("ABORTED", "HEAD moved during the rebuild")
    git(top, "reset", "-q", "--soft", new)
    return f"SHAPED {count} commits", log


def remove_worktree(top, wt):
    if raw(top, "worktree", "remove", "--force", wt).returncode:
        shutil.rmtree(wt, ignore_errors=True)
        raw(top, "worktree", "prune")


def run(manifest_path):
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    done = raw(os.getcwd(), "rev-parse", "--show-toplevel")
    if done.returncode:
        raise Stop("ABORTED", "not in a git repository")
    top = done.stdout.strip()
    check_manifest(manifest)
    start, mb, shas = preflight(top, manifest)
    branch = git(top, "symbolic-ref", "HEAD").strip()
    bumps, doc_steps, purposes, left, test_step, orphans = plan(top, manifest, start, mb, shas)
    wt = tempfile.mkdtemp()
    try:
        git(top, "worktree", "add", "-q", "--detach", wt, mb)
        build(wt, bumps, doc_steps, purposes, left, test_step, orphans, start, mb)
        return verify(top, branch, start, mb, git(wt, "rev-parse", "HEAD").strip())
    finally:
        remove_worktree(top, wt)


def interrupted(signum, _frame):
    raise Stop("ABORTED", f"interrupted by signal {signum}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    code, detail = 0, ""
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, interrupted)
    try:
        if len(argv) != 1:
            raise Stop("ABORTED", "usage: reshape.py <manifest>")
        line, detail = run(argv[0])
    except Stop as stop:
        line, detail = f"{stop.outcome} {stop.reason}", stop.detail
        code = 1 if stop.outcome == "ABORTED" else 0
    except BaseException as error:  # the HISTORY: line is the contract, whatever broke
        line, code = f"ABORTED unexpected {type(error).__name__}: {error}", 1
    sys.stdout.reconfigure(errors="replace")
    if detail:
        print(detail.rstrip("\n"))
    print("HISTORY: " + " ".join(line.split()), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
