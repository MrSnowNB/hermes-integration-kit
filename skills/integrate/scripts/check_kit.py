#!/usr/bin/env python3
"""Check that the kit is consistent and its executable parts work.

Exit 0 when every check passes, 1 otherwise. Standard library only.
"""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

SKILL = Path(__file__).resolve().parent.parent
KIT = SKILL.parent.parent
SCRIPTS = SKILL / "scripts"
RUNNER = SCRIPTS / "toolchain_harness.py"
REFERENCE = SKILL / "examples" / "reference"
DENY_PATTERNS = [re.compile(p) for p in (
    r"sk-lf-[A-Za-z0-9]{8,}", r"pk-lf-[A-Za-z0-9]{8,}", r"\bsk-[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----")]
DENY_FILES = {".env", "auth.json", "honcho.json", "state.db"}
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True,
                          text=True, cwd=cwd, timeout=300)


def main():
    proc = run(RUNNER, "--self-test")
    check("runner self-tests", proc.returncode == 0, proc.stderr.strip().splitlines()[-1:])

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        proc = run(RUNNER, REFERENCE / "suite.json", "--evidence", tmp / "ev")
        report = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {}
        check("reference suite all cases match", proc.returncode == 0 and
              report.get("passed") == report.get("cases") == 4,
              f"exit {proc.returncode}, {report.get('passed')}/{report.get('cases')}")

        proc = run(RUNNER, REFERENCE / "suite.json", "--job", REFERENCE / "job.json",
                   "--evidence", tmp / "ev")
        check("reference live job passes", proc.returncode == 0, f"exit {proc.returncode}")

        project = tmp / "project"
        (project / ".git").mkdir(parents=True)
        proc = run(SCRIPTS / "scaffold.py", "--project", project, "--component",
                   "demo-tool", "--purpose", "Demo", "--upstream", "https://example.invalid")
        folder = project / "integrations" / "demo-tool"
        check("scaffold creates integration", proc.returncode == 0 and all(
            (folder / p).is_file() for p in ("README.md", "wrapper/adapter.py",
                                              "synthetic/suite.json", "job/job.json")))
        check("scaffold writes ledger", "| demo-tool | proposed |" in
              (project / "integrations" / "LEDGER.md").read_text())
        proc = run(SCRIPTS / "scaffold.py", "--project", project, "--component",
                   "demo-tool", "--purpose", "Demo")
        check("scaffold refuses overwrite", proc.returncode == 1)
        proc = run(RUNNER, folder / "synthetic" / "suite.json", "--evidence", tmp / "ev2")
        check("unimplemented adapter fails closed", proc.returncode != 0,
              f"exit {proc.returncode}")
        leftover = [p for p in folder.rglob("*") if p.is_file() and "{{" in p.read_text()]
        check("templates fully rendered", not leftover, [str(p) for p in leftover])

    catalog = json.loads((SKILL / "references" / "catalog.json").read_text())
    ids = [c["id"] for c in catalog["components"]]
    check("catalog ids unique", len(ids) == len(set(ids)))
    labels = {"verified-local", "verified-upstream", "verified-both", "inferred",
              "untested", "obsolete"}
    for c in catalog["components"]:
        exits = {s["expected_exit"] for s in c["synthetic_cases"]}
        check(f"catalog {c['id']} has 3+ cases and a non-pass case",
              len(c["synthetic_cases"]) >= 2 and exits != {0} and
              (len(c["synthetic_cases"]) >= 3 or c["id"] == "session-export"))
        check(f"catalog {c['id']} evidence label valid", c["evidence"] in labels)
        unknown = [d for d in c["depends_on"] + c["requires_any"] if d not in ids]
        check(f"catalog {c['id']} dependencies exist", not unknown, unknown)
        if c["evidence"].startswith("verified-upstream"):
            check(f"catalog {c['id']} cites upstream", bool(c["upstream"]))

    spec = importlib.util.spec_from_file_location("render", SCRIPTS / "render_tool_notes.py")
    render = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(render)
    for name, text in render.notes(catalog).items():
        note = KIT / "vault" / "tools" / f"{name}.md"
        check(f"vault note {name} matches catalog", note.is_file() and note.read_text() == text)

    vault_notes = {p.stem for p in (KIT / "vault").rglob("*.md")}
    for p in (KIT / "vault").rglob("*.md"):
        broken = [l for l in re.findall(r"\[\[([^\]|#]+)", p.read_text())
                  if l.split("/")[-1] not in vault_notes]
        check(f"links resolve in {p.relative_to(KIT)}", not broken, broken)

    skill_text = (SKILL / "SKILL.md").read_text()
    front = skill_text.split("---")[1]
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    check("SKILL.md has name and description", re.search(r"^name:\s*integrate$", front, re.M)
          and desc)
    check("SKILL.md description within 60 characters", desc and len(desc.group(1)) <= 60)
    for section in ("## When to Use", "## Procedure", "## Pitfalls", "## Verification"):
        check(f"SKILL.md has {section}", section in skill_text)
    for ref in re.findall(r"`((?:references|scripts|templates|examples)/[^`\s]+)`", skill_text):
        check(f"SKILL.md reference exists: {ref}", (SKILL / ref).exists())

    tracked = subprocess.run(["git", "ls-files"], cwd=KIT, capture_output=True, text=True)
    files = ([KIT / f for f in tracked.stdout.split()] if tracked.returncode == 0 and
             tracked.stdout.strip() else [p for p in KIT.rglob("*") if ".git" not in p.parts])
    for f in files:
        if not f.is_file():
            continue
        check(f"not a denied file: {f.name}", f.name not in DENY_FILES and
              not f.name.endswith(".gguf"))
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            continue
        hits = [p.pattern for p in DENY_PATTERNS if p.search(text)]
        check(f"no secret patterns in {f.relative_to(KIT)}", not hits, hits)
        if f.suffix == ".md" and "examples" not in f.parts:
            check(f"no em dashes in {f.relative_to(KIT)}", "\u2014" not in text)

    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        if not ok:
            print(f"FAIL  {name}  {detail}")
    print(f"{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
