---
title: "Tool: Domain metric slot (example: TrackEval for multi-object tracking)"
type: tool
status: draft
evidence: verified-upstream
layer: 4
sources:
  - "https://github.com/JonathonLuiten/TrackEval"
  - "https://github.com/JonathonLuiten/TrackEval/blob/master/docs/MOTChallenge-format.txt"
secrets: false
---

# Domain metric slot (example: TrackEval for multi-object tracking)

Score a model pipeline with the field's standard metric instead of a generic one.

## Use when

- The project outputs something a field already measures: tracks, retrieval, detection, transcription.
- You need regression checks per category.

## Avoid when

- No labeled ground truth exists yet. Build it first.
- You only need agent-procedure checks.

## What it proves

- **Proves:** Metric movement on planted faults in the expected direction.
- **Does not prove:** Accuracy on real footage until labeled real data passes.
- **Gate type:** deterministic threshold per category

## How it attaches to Hermes

Cron job or CI step over a labeled golden folder

Depends on: [[contract-runner]]

## Synthetic acceptance

| Case | Input | Exit | Expected |
|---|---|---|---|
| `TRACK-PERFECT` | Tracker output identical to ground truth | 0 | pass, HOTA near 1.0 |
| `TRACK-SWAP` | IDs swapped halfway | 1 | block, association metrics drop |
| `TRACK-FRAME-ZERO` | Frames numbered from 0 | 2 | error, frames must be 1-based |

## Typical job

Watch the golden folder for new labeled clips, score them, append per-clip metrics to a CSV.

## Upstream

- https://github.com/JonathonLuiten/TrackEval
- https://github.com/JonathonLuiten/TrackEval/blob/master/docs/MOTChallenge-format.txt

## Ran

Evidence `verified-upstream`. Awaiting a run on a target host. Record date, host, and evidence path here.

Then [[human-agreement]].
