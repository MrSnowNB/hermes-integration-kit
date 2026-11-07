# Sequential rollout

One component at a time. Each one produces something the next one uses. A
component is not started until the one before it is admitted, unless the
catalog lists no dependency between them.

## Layers

| Layer | Component | Why it comes here |
|---|---|---|
| 0 | contract-runner, session-export | Every later gate runs through the runner. Exported sessions are the first stable trace source. |
| 1 | langfuse-trace | See what agents do across many runs before judging them. Observer only. |
| 2 | pairwise-fixtures | Deterministic project checks need no traces and unblock product work soonest. |
| 3 | tool-correctness | Needs exported sessions and a golden tool sequence. |
| 4 | domain-metric | Needs labeled ground truth for the project's own output. |
| 5 | human-agreement | Confirms the labels behind layer 4 and any judge are measurable. |
| 6 | runtime-guard | Added once you know which tool calls must never happen. |
| 7 | failure-harvest | Needs at least one admitted gate producing failures. |

Layers 1 and 2 can swap. Product projects without agent-trace needs often
start at 2. Layers 4 and 5 apply only when the project ships a model
pipeline. Skip a layer by recording `skipped` and the reason in the ledger.

## States

`proposed` → `pinned` → `synthetic-green` → `job-green` → `admitted`

Also `paused` (blocked on an outside dependency) and `retired` (removed, with
the reason). Only the operator sets `admitted` or `retired`.

## Promotion gate, every component

| Check | Required |
|---|---|
| Gate written and approved | Before code |
| Upstream pinned | Exact version or commit SHA, host, date |
| Synthetic suite | At least one pass, one planted block, one error; all match |
| Expected results | Written before the first run |
| Live job | Two clean runs, evidence saved |
| Privacy | What the tool sees and where it stores it, written down |
| Rollback | One step, tested once |
| Operator sign-off | Recorded in the ledger |

## Rollback triggers

- A synthetic case that passed now fails after a version change.
- A live job errors twice in a row.
- A tool exports data the Gate did not allow.

Rollback means: unpin, remove the Hermes surface attachment, set the ledger
row to `paused`, and write the reason in the project inbox.

## Adding a component that is not in the catalog

1. Write a catalog entry in a branch: purpose, use_when, avoid_when, proves,
   does_not_prove, gate_type, hermes_surface, depends_on, upstream, evidence
   `untested`, at least three synthetic cases, one sample job.
2. The operator reviews the entry.
3. Follow the normal procedure from Propose.
