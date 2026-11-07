#!/usr/bin/env python3
"""Render one Obsidian tool note per catalog component.

The catalog is the source of truth. Rerun this after editing it, then commit
both. `check_kit.py` fails if the notes drift from the catalog.

    python render_tool_notes.py --catalog references/catalog.json --out ../../vault/tools
"""
import argparse
import json
from pathlib import Path
import sys


def render(component, next_id):
    c = component
    sources = "".join(f'\n  - "{u}"' for u in c["upstream"])
    sources = f"sources:{sources}" if sources else "sources: []"
    deps = ", ".join(f"[[{d}]]" for d in c["depends_on"]) or "none"
    if c["requires_any"]:
        deps += "; plus one of " + ", ".join(f"[[{d}]]" for d in c["requires_any"])
    cases = "\n".join(f"| `{s['id']}` | {s['input']} | {s['expected_exit']} | {s['expected']} |"
                      for s in c["synthetic_cases"])
    use = "\n".join("- " + x for x in c["use_when"])
    avoid = "\n".join("- " + x for x in c["avoid_when"]) or "- Never skip it."
    links = "\n".join("- " + u for u in c["upstream"]) or "- None. Built in this kit."
    ran = ("Ran in this kit; see the reference suite." if c["evidence"] == "verified-local"
           else "Awaiting a run on a target host. Record date, host, and evidence path here.")
    then = f"Then [[{next_id}]]." if next_id else "This is the last layer. Return to [[eval-loop]]."
    return f"""---
title: "Tool: {c['name']}"
type: tool
status: draft
evidence: {c['evidence']}
layer: {c['layer']}
{sources}
secrets: false
---

# {c['name']}

{c['purpose']}

## Use when

{use}

## Avoid when

{avoid}

## What it proves

- **Proves:** {c['proves']}
- **Does not prove:** {c['does_not_prove']}
- **Gate type:** {c['gate_type']}

## How it attaches to Hermes

{c['hermes_surface']}

Depends on: {deps}

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
{cases}

## Typical job

{c['sample_job']}

## Upstream

{links}

## Ran

Evidence `{c['evidence']}`. {ran}

{then}
"""


def notes(catalog):
    comps = catalog["components"]
    return {c["id"]: render(c, comps[i + 1]["id"] if i + 1 < len(comps) else None)
            for i, c in enumerate(comps)}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, text in notes(json.loads(Path(args.catalog).read_text())).items():
        (out / f"{name}.md").write_text(text)
        print(out / f"{name}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
