---
name: integrate
description: Add one toolchain component to a Hermes project
version: 0.1.0
author: MrSnowNB
metadata:
  hermes:
    category: devops
    tags: [integration, evaluation, toolchain, harness]
---

# Integrate

Add one toolchain component to a Hermes project, prove it on synthetic
fixtures with known answers, then show it working on one real job. One
component at a time. The model proposes. The gate and the operator authorize.

## When to Use

- The operator asks to add, wire up, or evaluate a tool, plugin, metric, or
  checker in a Hermes project.
- A project needs tracing, trajectory scoring, fixture generation, a domain
  metric, human-agreement checks, or failure harvesting.
- An existing integration needs a version bump or has broken.

Do not use this skill to install software the operator has not approved, to
build product features, or to run several new components at once.

## Procedure

Read `references/rollout.md` once per project. Then, for each component:

1. **Choose.** Read `references/catalog.json`. Pick the next component whose
   `depends_on` entries are all `admitted` in `integrations/LEDGER.md`. Use the
   `use_when` and `avoid_when` fields. If none fits, write the gap to the
   project inbox and stop.
2. **Propose.** Run `scripts/scaffold.py --project <root> --component <name>
   --purpose "<one sentence>" --upstream <official doc URL>`. Fill in the
   Gate section of the new README. Ask the operator to approve the Gate
   before writing code.
3. **Pin.** After approval, install the exact upstream version. Record the
   version, host, date, and install command in the Pin table. Set the ledger
   row to `pinned`. Installing anything requires operator approval.
4. **Synthetic.** Replace every `todo` fixture. Each suite needs at least one
   pass case, one planted fault that must block, and one input that must
   error. Write expected results before running the tool. Implement
   `wrapper/adapter.py` against `references/adapter-contract.md`. Run
   `scripts/toolchain_harness.py integrations/<name>/synthetic/suite.json`.
   All cases must match. Set the row to `synthetic-green`.
5. **Job.** Fill in `job/job.json` with one typical real use. Run it with
   `--job`. It must pass twice, on separate runs, with evidence saved. Attach
   it to a Hermes surface only as described in `references/hermes-surfaces.md`.
   Set the row to `job-green`.
6. **Admit.** Show the operator the Gate, both evidence paths, and any
   failures seen. Only the operator sets `admitted`. Then write the tool note
   in the project vault and name the next component in `## Then`.

## Pitfalls

- Never edit a fixture or expected result to make a failing run pass. A
  wrong fixture is fixed in a separate, reviewed change.
- Fail-open tools cannot gate. The Langfuse plugin and default shell hooks
  proceed on error. A gate needs a fail-closed check: CI exit code, a
  `pre_tool_call` shell hook with `fail_closed: true`, or this runner.
- Do not read `~/.hermes/state.db` from a gate. Its schema changes between
  releases. Use `hermes sessions export` or the trace backend.
- A cron job created inside a profile session is stored in that profile.
  Confirm it with `hermes cron list` under the profile the gateway serves.
- Synthetic success proves the wiring and the metric arithmetic. It does not
  prove quality on real data. Say so in the Gate.
- Credentials, session stores, and model weights never enter the repository.
  See `DENY.txt` at the kit root.

## Verification

- `scripts/toolchain_harness.py --self-test` passes.
- The component's synthetic suite returns exit 0 with every case `pass`,
  including the block and error cases.
- Two live job runs return exit 0 with `results.json` saved.
- `integrations/LEDGER.md` shows the current state, pin, and evidence path.
