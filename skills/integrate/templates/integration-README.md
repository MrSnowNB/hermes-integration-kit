---
title: "{{component}}"
type: integration
status: draft
state: proposed
evidence: untested
created: "{{date}}"
upstream: "{{upstream}}"
pin: "TODO: exact version, tag, or commit SHA"
secrets: false
---

# {{component}}

{{purpose}}

## Gate

Written before any code. The operator approves this section.

- **Proves:** TODO, one sentence on what a pass means.
- **Does not prove:** TODO, the claim this component cannot support.
- **Inputs:** TODO
- **Outputs:** the standard envelope plus TODO artifacts.
- **Pass:** TODO, measurable threshold.
- **Block:** TODO, the planted fault that must be caught.
- **Error:** TODO, input the tool cannot judge.
- **Privacy:** TODO, what data the tool sees and where it is stored.
- **Rollback:** TODO, the one step that removes this component.

## Pin

| Field | Value |
|---|---|
| Upstream | {{upstream}} |
| Version | TODO |
| Installed on | TODO host and date |
| Install command | TODO |

## Runs

Record each run with date, host, command, and the results.json path.

| Date | Mode | Host | Result | Evidence |
|---|---|---|---|---|

## Then

The next component in the rollout, once this one is admitted.
