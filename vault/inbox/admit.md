---
title: "How a component is admitted"
type: instruction
status: draft
evidence: untested
verified_on: "2026-11-07"
secrets: false
---

# How a component is admitted

Follow [[new-integration]]. Admission holds when all of these exist in the
project:

- `integrations/<component>/README.md` with an approved Gate and a Pin.
- A synthetic suite with a pass case, a planted block, and an error case,
  every case matching.
- Two clean live job runs with saved `results.json`.
- A written privacy line and a one-step rollback.
- A ledger row the operator moved to `admitted`.

Then the operator updates the component's note in `tools/` with the host,
date, and evidence path, and the evidence label becomes `verified-both`.

One component per change. A change that admits two components is split.
