---
title: "When to use each component"
type: foundation
status: draft
evidence: verified-upstream
verified_on: "2026-11-07"
sources:
  - "https://hermes-agent.nousresearch.com/docs/plugins/langfuse"
  - "https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks"
  - "https://deepeval.com/docs/metrics-tool-correctness"
  - "https://github.com/thombashi/allpairspy"
  - "https://github.com/JonathonLuiten/TrackEval"
  - "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html"
  - "https://pmc.ncbi.nlm.nih.gov/articles/PMC7619182/"
secrets: false
---

# When to use each component

Start from the question you need answered. Pick the one component that
answers it. Add the next only when this one is admitted.

| If you need to know... | Use | Not this |
|---|---|---|
| Does an adapter behave as specified? | [[contract-runner]] | Manual spot checks |
| Which tools did a run call, in order? | [[session-export]] | Reading `state.db` directly |
| What are agents doing across many runs, and what does it cost? | [[langfuse-trace]] | A gate. It is fail-open. |
| Does my parser or form handle every pair of input variations? | [[pairwise-fixtures]] | Exhaustive combinations |
| Did the agent follow the verified procedure, or loop and skip? | [[tool-correctness]] | Scoring open-ended work by sequence |
| Is the model pipeline's output good by the field's own measure? | [[domain-metric]] | Generic LLM-judge scores |
| Do people even agree on this label? Is a judge's rate trustworthy? | [[human-agreement]] | Raw percent agreement |
| Must a tool call be stopped before it happens? | [[runtime-guard]] | CI, which runs too late |
| How do failures become permanent tests? | [[failure-harvest]] | Automatic promotion |

## Three questions before any component

1. **Is it a record or a gate?** Records can fail open. Gates must fail
   closed. If a record matters to a decision, add a gate that checks it.
2. **What does synthetic success prove?** Wiring and arithmetic. Not quality
   on real data. Write that limit in the Gate.
3. **Who sees the data?** Write it down before the first run. For private or
   minor data, use metadata-only capture and keep media off the trace.

## Typical starting points

- **New agent-built app.** [[contract-runner]], then [[pairwise-fixtures]]
  on the first input format, then [[session-export]] and
  [[tool-correctness]] on agent PRs.
- **Agent operations on a fleet.** [[contract-runner]], [[langfuse-trace]]
  self-hosted, then [[runtime-guard]] for the calls that must never happen.
- **Model pipeline with human review.** [[contract-runner]],
  [[human-agreement]] on the labels first, then [[domain-metric]], then
  [[failure-harvest]].

The full layer order and promotion gate are in
`../skills/integrate/references/rollout.md`.
