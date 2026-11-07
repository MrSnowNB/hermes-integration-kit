---
title: "eval-loop"
type: chain
status: draft
evidence: untested
verified_on: "2026-11-07"
secrets: false
tools:
  - "[[session-export]]"
  - "[[langfuse-trace]]"
  - "[[tool-correctness]]"
  - "[[runtime-guard]]"
  - "[[failure-harvest]]"
---

# eval-loop

The steady state once several components are admitted. Agents run. Runs are
recorded. Gates score them. Failures are harvested. A person promotes.

1. A Hermes session runs with [[runtime-guard]] active, so forbidden calls
   are blocked as they happen.
2. [[langfuse-trace]] records the run. [[session-export]] produces the stable
   record a gate reads.
3. In CI, [[tool-correctness]] and the project's own tests score the change.
   The contract runner's exit code decides whether it merges.
4. [[failure-harvest]] scrubs and deduplicates the failures and lists them in
   the inbox.
5. The operator promotes a harvested case to a golden fixture, or drops it.

Projects with a model pipeline add [[domain-metric]] at step 3, and run
[[human-agreement]] before trusting any new label set.

## Ran

Awaiting a project with all listed components admitted.
