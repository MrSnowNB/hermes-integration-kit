---
title: "Tool: Pairwise fixture generation (allpairspy)"
type: tool
status: draft
evidence: verified-upstream
layer: 2
sources:
  - "https://github.com/thombashi/allpairspy"
secrets: false
---

# Pairwise fixture generation (allpairspy)

Generate a small fixture set that covers every pair of input variations for a parser or form.

## Use when

- An input has several independent dimensions (format, encoding, blanks, quoting).
- Exhaustive combinations are too many to keep.

## Avoid when

- Faults depend on three or more factors at once. Use n-wise or targeted cases.
- The input has one or two dimensions. Write the cases by hand.

## What it proves

- **Proves:** That the code under test handles each generated fixture as its expected.json says.
- **Does not prove:** Optimal coverage. The upstream project calls its output good enough, not optimal.
- **Gate type:** deterministic, fail-closed

## How it attaches to Hermes

Pre-commit hook or CI step. Fixture folders are read-only to the coding agent.

Depends on: [[contract-runner]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `PAIRS-COVER` | 5 dimensions with known values | 0 | pass, every value pair appears at least once |
| `PAIRS-SHORT-ROW` | Fixture with a row missing columns | 1 | block, readable row error, no stack trace |
| `PAIRS-EMPTY` | Zero-byte file | 1 | block, EMPTY_INPUT |

## Typical job

Pre-commit: run the parser over the golden fixture folder and fail on any mismatch.

## Upstream

- https://github.com/thombashi/allpairspy

## Ran

Evidence `verified-upstream`. Awaiting a run on a target host. Record date, host, and evidence path here.

Then [[tool-correctness]].
