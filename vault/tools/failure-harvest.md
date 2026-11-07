---
title: "Tool: Failure harvesting"
type: tool
status: draft
evidence: untested
layer: 7
sources: []
secrets: false
---

# Failure harvesting

Turn gate failures and human corrections into reviewable candidate fixtures.

## Use when

- At least one gate is admitted and producing failures.
- You want regressions to become permanent tests.

## Avoid when

- No gate is admitted yet. There is nothing to harvest.
- Promotion would be automatic. Promotion stays with the operator.

## What it proves

- **Proves:** That failures are deduplicated, scrubbed of secrets and personal data, and queued for review.
- **Does not prove:** That a harvested case is a correct golden. A person decides.
- **Gate type:** deterministic scrub and dedupe; human promotion

## How it attaches to Hermes

Weekly cron that lists pending cases in the vault inbox

Depends on: [[contract-runner]]; plus one of [[tool-correctness]], [[pairwise-fixtures]], [[domain-metric]], [[human-agreement]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `HARVEST-DEDUP` | Two near-identical failures and one distinct failure | 0 | pass, 2 pending cases |
| `HARVEST-SECRET` | Failure containing a planted API-key canary | 0 | pass, canary absent from the pending file |
| `HARVEST-NO-APPROVAL` | Request to promote without an operator approval record | 1 | block, APPROVAL_REQUIRED |

## Typical job

Weekly: list pending cases in the vault inbox for review.

## Upstream

- None. Built in this kit.

## Ran

Evidence `untested`. Awaiting a run on a target host. Record date, host, and evidence path here.

This is the last layer. Return to [[eval-loop]].
