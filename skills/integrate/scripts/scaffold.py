#!/usr/bin/env python3
"""Scaffold one toolchain integration inside a target project.

Creates integrations/<component>/ with a README gate, a fail-closed adapter
skeleton, a synthetic suite (pass, block, error), and a live job template, then
records the component as `proposed` in integrations/LEDGER.md.

It never overwrites an existing integration folder.

    python scaffold.py --project /path/to/repo --component langfuse-trace \
        --purpose "Trace Hermes turns and tool calls" --upstream https://...
"""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"
LEDGER_HEADER = """# Integration ledger

One row per component. States move in order: proposed, pinned,
synthetic-green, job-green, admitted. A component can also be paused or
retired. Only the operator moves a row to admitted.

| Component | State | Pin | Updated | Evidence |
|---|---|---|---|---|
"""


def render(name, **values):
    text = (TEMPLATES / name).read_text()
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", required=True, help="Target project root")
    parser.add_argument("--component", required=True, help="Lowercase name, e.g. langfuse-trace")
    parser.add_argument("--purpose", required=True, help="One sentence: what this component proves")
    parser.add_argument("--upstream", default="", help="Official documentation URL")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", args.component):
        print("component must be lowercase letters, digits, and hyphens", file=sys.stderr)
        return 2
    project = Path(args.project).resolve()
    if not (project / ".git").exists():
        print("project root must be a Git checkout", file=sys.stderr)
        return 2
    root = project / "integrations"
    folder = root / args.component
    if folder.exists():
        print(f"{folder} already exists; refusing to overwrite", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    values = {"component": args.component, "purpose": args.purpose,
              "upstream": args.upstream or "TODO: official documentation URL",
              "date": today}
    for sub in ("wrapper", "synthetic", "job"):
        (folder / sub).mkdir(parents=True)
    (folder / "README.md").write_text(render("integration-README.md", **values))
    adapter = folder / "wrapper" / "adapter.py"
    adapter.write_text(render("adapter.py", **values))
    adapter.chmod(0o755)
    (folder / "synthetic" / "suite.json").write_text(
        render("suite.json", **values))
    (folder / "job" / "job.json").write_text(render("job.json", **values))

    ledger = root / "LEDGER.md"
    if not ledger.exists():
        ledger.write_text(LEDGER_HEADER)
    with ledger.open("a") as stream:
        stream.write(f"| {args.component} | proposed | none | {today} | none |\n")

    print(json.dumps({"status": "pass", "created": str(folder.relative_to(project)),
                      "next_actions": [
                          "Pin the upstream version in README.md",
                          "Replace TODO fixtures in synthetic/suite.json",
                          "Implement wrapper/adapter.py",
                      ]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
