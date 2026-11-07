---
title: "Schema"
type: foundation
status: draft
evidence: untested
verified_on: "2026-11-07"
secrets: false
---

# SCHEMA

## Evidence labels

Required on every tool, toolchain, and runbook note.

| Label | Meaning |
|---|---|
| `verified-local` | Run on a named host, with date, command, and evidence path |
| `verified-upstream` | Command or behavior stated in linked official docs |
| `verified-both` | Both of the above |
| `inferred` | Plausible, awaiting a check |
| `untested` | Proposed procedure or config, awaiting a run |
| `obsolete` | Historical. Revalidate before use. |

A component moves from `verified-upstream` to `verified-both` only after its
synthetic suite and two live jobs pass on a named host.

## Integration states

`proposed`, `pinned`, `synthetic-green`, `job-green`, `admitted`, plus
`paused`, `skipped`, and `retired`. States live in each project's
`integrations/LEDGER.md`.

## Write policy

Agents write `inbox/` on their own. Everything else waits for the operator.

## Provenance frontmatter

```yaml
---
title: "..."
type: tool | chain | foundation | runbook | decision | instruction | draft
status: draft | verified | obsolete
evidence: verified-local | verified-upstream | verified-both | inferred | untested
verified_on: YYYY-MM-DD
sources: []
secrets: false
---
```

## Source of truth

`../skills/integrate/references/catalog.json` defines the components. The
notes in `tools/` are rendered from it with
`../skills/integrate/scripts/render_tool_notes.py`. Edit the catalog, then
rerun the renderer. `check_kit.py` fails on drift.

## Secrets

`secrets: false` on every note. See `../DENY.txt`.
