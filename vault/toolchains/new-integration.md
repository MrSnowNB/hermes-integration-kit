---
title: "new-integration"
type: chain
status: draft
evidence: untested
verified_on: "2026-11-07"
secrets: false
tools:
  - "[[contract-runner]]"
---

# new-integration

Choose, propose, pin, synthetic, job, admit. The note is the order.

1. **Choose** the next component from [[when-to-use]] whose dependencies are
   admitted.
2. **Propose.** `scaffold.py` creates `integrations/<component>/`. Fill in
   the Gate. The operator approves it.
3. **Pin** the exact upstream version after the operator approves the
   install.
4. **Synthetic.** Write expected results, then fixtures, then the adapter.
   Run the suite with [[contract-runner]]. Every case must match.
5. **Job.** Run one typical real job twice with `--job`.
6. **Admit.** The operator reviews the evidence and sets `admitted`. See
   [[admit]].

```text
python skills/integrate/scripts/scaffold.py --project <repo> \
  --component <name> --purpose "<one sentence>" --upstream <doc URL>
python skills/integrate/scripts/toolchain_harness.py \
  <repo>/integrations/<name>/synthetic/suite.json --evidence <repo>/evidence
python skills/integrate/scripts/toolchain_harness.py \
  <repo>/integrations/<name>/synthetic/suite.json \
  --job <repo>/integrations/<name>/job/job.json --evidence <repo>/evidence
```

## Ran

2026-11-07, kit build sandbox. The scaffold, the fail-closed skeleton, and
the reference suite ran. No vendor component has run through this chain yet.
