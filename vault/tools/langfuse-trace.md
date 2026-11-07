---
title: "Tool: Langfuse tracing via the Hermes plugin"
type: tool
status: draft
evidence: verified-upstream
layer: 1
sources:
  - "https://hermes-agent.nousresearch.com/docs/plugins/langfuse"
  - "https://langfuse.com/docs/observability/features/masking"
  - "https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks"
secrets: false
---

# Langfuse tracing via the Hermes plugin

Record turns, LLM calls, tool calls, tokens, and cost for every run.

## Use when

- You need to see what an agent did across many runs.
- You need cost or latency per turn.
- You want failed sessions to become dataset items.

## Avoid when

- You need to block anything. The plugin is fail-open.
- The data includes minors or private content and capture mode has not been set to metadata.

## What it proves

- **Proves:** That a run produced the expected trace shape without leaking planted canaries.
- **Does not prove:** That traces are complete. A full queue, failed export, or abrupt kill can lose telemetry.
- **Gate type:** fail-open observer. The adapter checks trace presence and fails closed on its own.

## How it attaches to Hermes

Plugin: hermes plugins install langfuse; HERMES_LANGFUSE_BASE_URL for self-hosted; HERMES_LANGFUSE_CAPTURE=metadata|sanitized|full

Depends on: [[contract-runner]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `TRACE-OK` | Scripted session: 1 turn, 1 generation, 3 tool calls, 3 planted canaries, capture metadata | 0 | pass, tool_calls = 3, canary_leaks = 0 |
| `TRACE-MISSING` | Same session with keys unset | 2 | error, NO_TRACE. Hermes itself still completes the turn. |
| `TRACE-LEAK` | Capture full with a canary in the prompt | 1 | block, CANARY_LEAK |

## Typical job

Nightly: summarize yesterday's traces per session (model, tool calls, tokens, cost) into the vault inbox.

## Upstream

- https://hermes-agent.nousresearch.com/docs/plugins/langfuse
- https://langfuse.com/docs/observability/features/masking
- https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks

## Ran

Evidence `verified-upstream`. Awaiting a run on a target host. Record date, host, and evidence path here.

Then [[pairwise-fixtures]].
