---
title: "Tool: Hermes session export"
type: tool
status: draft
evidence: verified-upstream
layer: 0
sources:
  - "https://hermes-agent.nousresearch.com/docs/reference/cli-commands"
secrets: false
---

# Hermes session export

Produce a stable JSONL record of sessions, messages, and tool calls for offline scoring.

## Use when

- A gate needs the tool-call sequence of a Hermes run.
- No trace backend is installed yet.

## Avoid when

- You need live dashboards or cost tracking across many runs. Add langfuse-trace.

## What it proves

- **Proves:** Which tools a session called, in which order.
- **Does not prove:** That the session's output was correct.
- **Gate type:** input source, not a gate

## How it attaches to Hermes

CLI: hermes sessions export <output> [--session-id ID]

Depends on: [[contract-runner]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `EXPORT-SHAPE` | A scripted session with three known tool calls | 0 | pass, tool_calls = 3, order preserved |
| `EXPORT-EMPTY` | A session ID that does not exist | 2 | error, NO_SESSION |

## Typical job

Export yesterday's sessions for one profile and count tool calls per session.

## Upstream

- https://hermes-agent.nousresearch.com/docs/reference/cli-commands

## Ran

Evidence `verified-upstream`. Awaiting a run on a target host. Record date, host, and evidence path here.

Then [[langfuse-trace]].
