---
title: "Tool: Runtime guard (Hermes pre_tool_call shell hook, fail-closed)"
type: tool
status: draft
evidence: verified-upstream
layer: 6
sources:
  - "https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks"
secrets: false
---

# Runtime guard (Hermes pre_tool_call shell hook, fail-closed)

Block a specific risky tool call while the agent runs, not after.

## Use when

- A tool call must never happen: writing fixtures, touching credentials, deleting outside the workdir.
- CI is too late to stop the harm.

## Avoid when

- The rule is a quality score. Score it in CI.
- The hook is slow. Default timeout is 60 seconds, capped at 300.

## What it proves

- **Proves:** That a planted forbidden call is blocked and an allowed call proceeds.
- **Does not prove:** Coverage of calls the matcher does not match.
- **Gate type:** fail-closed only with fail_closed: true

## How it attaches to Hermes

Shell hook in the profile config.yaml; verify with hermes hooks test and hermes hooks doctor

Depends on: [[contract-runner]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `GUARD-ALLOW` | Synthetic pre_tool_call payload for an allowed path | 0 | pass, hook returns {} |
| `GUARD-BLOCK` | Payload that edits a read-only fixture folder | 1 | block, decision block with reason |
| `GUARD-CRASH` | Hook script that exits non-zero with no directive | 1 | block, because fail_closed is set |

## Typical job

Guard the golden fixture folders in every coding session.

## Upstream

- https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks

## Ran

Evidence `verified-upstream`. Awaiting a run on a target host. Record date, host, and evidence path here.

Then [[failure-harvest]].
