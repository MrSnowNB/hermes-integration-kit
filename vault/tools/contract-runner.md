---
title: "Tool: Contract-test runner"
type: tool
status: draft
evidence: verified-local
layer: 0
sources: []
secrets: false
---

# Contract-test runner

Run synthetic suites and live jobs through adapters and save evidence.

## Use when

- Always. Every other component is tested through it.

## Avoid when

- Never skip it.

## What it proves

- **Proves:** An adapter returns the expected status, exit code, metrics, and artifacts for a fixture.
- **Does not prove:** That the wrapped tool is correct on real data.
- **Gate type:** deterministic, fail-closed

## How it attaches to Hermes

CI step, pre-commit hook, or a no-agent cron script

Depends on: none

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `KEYS-OK` | Document with all required keys | 0 | pass, missing = 0 |
| `KEYS-MISSING` | Document missing two keys | 1 | block, MISSING_KEYS, missing = 2 |
| `KEYS-NOT-OBJECT` | A JSON list | 2 | error, NOT_OBJECT |

## Typical job

examples/reference/job.json: check a real config file for required keys.

## Upstream

- None. Built in this kit.

## Ran

Evidence `verified-local`. Ran in this kit; see the reference suite.

Then [[session-export]].
