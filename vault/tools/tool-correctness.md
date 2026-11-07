---
title: "Tool: Trajectory scoring (DeepEval ToolCorrectnessMetric)"
type: tool
status: draft
evidence: verified-upstream
layer: 3
sources:
  - "https://deepeval.com/docs/metrics-tool-correctness"
secrets: false
---

# Trajectory scoring (DeepEval ToolCorrectnessMetric)

Score whether a run called the expected tools, optionally in order.

## Use when

- A task has a verified procedure with a known tool sequence.
- You see loops, skipped steps, or extra tool calls.

## Avoid when

- Open-ended feature work where many sequences are valid. Score outcomes instead.
- You need an LLM judge to run offline. Leave available_tools unset to keep the score deterministic.

## What it proves

- **Proves:** Tool names, and optionally order or exact match, against a golden list.
- **Does not prove:** That the final output is right. Pair with the project's own tests.
- **Gate type:** deterministic when available_tools is not passed

## How it attaches to Hermes

CI step on each agent-authored PR, reading an exported session

Depends on: [[contract-runner]], [[session-export]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `TRAJ-OK` | Golden [read_file, edit_file, run_tests]; same trace | 0 | pass, score 1.0 |
| `TRAJ-LOOP` | read_file six times, then the golden sequence | 1 | block, STEP_EFFICIENCY |
| `TRAJ-SKIP` | Golden without run_tests | 1 | block, MISSING_TOOL |

## Typical job

CI: score the session attached to each PR and post score and reason as a comment.

## Upstream

- https://deepeval.com/docs/metrics-tool-correctness

## Ran

Evidence `verified-upstream`. Awaiting a run on a target host. Record date, host, and evidence path here.

Then [[domain-metric]].
