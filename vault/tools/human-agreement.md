---
title: "Tool: Human agreement and judge calibration (Cohen's kappa, Rogan-Gladen)"
type: tool
status: draft
evidence: verified-upstream
layer: 5
sources:
  - "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html"
  - "https://pmc.ncbi.nlm.nih.gov/articles/PMC7619182/"
secrets: false
---

# Human agreement and judge calibration (Cohen's kappa, Rogan-Gladen)

Check that people agree on a label before tuning a model or judge to it, then correct observed rates for known detector error.

## Use when

- A label is subjective (a coaching call, a rubric score).
- An LLM judge or detector reports a rate you plan to act on.

## Avoid when

- More than two annotators. sklearn kappa covers two.
- Detector sensitivity and specificity are unknown or sum to 1. The correction is undefined.

## What it proves

- **Proves:** Whether a label is measurable, and a corrected prevalence under stated error rates.
- **Does not prove:** That the corrected rate transfers to new data with different error rates.
- **Gate type:** deterministic threshold, human-labeled input

## How it attaches to Hermes

Agent task that reads two label exports and writes a vault note

Depends on: [[contract-runner]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `AGREE-HIGH` | Confusion matrix rows (48, 2) and (3, 47) | 0 | pass, kappa 0.90 |
| `AGREE-SKEW` | Confusion matrix rows (60, 20) and (20, 0), 60% raw agreement | 1 | block, kappa -0.25 |
| `AGREE-CORRECTION` | Observed 0.41, sensitivity 0.9, specificity 0.8 | 0 | pass, corrected prevalence 0.30 |
| `AGREE-DEGENERATE` | Sensitivity 0.5, specificity 0.5 | 2 | error, UNDEFINED_CORRECTION |

## Typical job

Compare two reviewers' tag exports, compute kappa per label, flag any label below threshold.

## Upstream

- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7619182/

## Ran

Evidence `verified-upstream`. Awaiting a run on a target host. Record date, host, and evidence path here.

Then [[runtime-guard]].
