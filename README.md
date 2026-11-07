# Hermes Integration Kit

A generic toolset for adding evaluation and control components to any Hermes
project, one component at a time. Each component is proven on synthetic
fixtures with known answers, then shown on one real job, before anyone
trusts it.

It has two audiences:

- **People** open `vault/` in Obsidian. It explains each component, when to
  use it, what it proves, and how it attaches to Hermes.
- **Agents** load `skills/integrate/` as the `integrate` skill. It gives the
  procedure, the contract runner, the scaffolder, and the templates.

## What is in it

| Path | What it is |
|---|---|
| `skills/integrate/SKILL.md` | Agent procedure: choose, propose, pin, synthetic, job, admit |
| `skills/integrate/references/catalog.json` | Source of truth for the nine components |
| `skills/integrate/references/rollout.md` | Layer order, states, promotion gate, rollback |
| `skills/integrate/references/adapter-contract.md` | Request, response, and exit-code contract |
| `skills/integrate/references/hermes-surfaces.md` | Plugins, hooks, skills, cron, CI, toolsets: which to use |
| `skills/integrate/scripts/toolchain_harness.py` | Contract runner, standard-library Python |
| `skills/integrate/scripts/scaffold.py` | Creates `integrations/<component>/` in a project |
| `skills/integrate/scripts/render_tool_notes.py` | Renders `vault/tools/` from the catalog |
| `skills/integrate/scripts/check_kit.py` | Verifies the kit is consistent |
| `skills/integrate/examples/reference/` | A working adapter, suite, and live job |
| `vault/foundations/when-to-use.md` | Decision guide for the toolset |
| `examples/attack-first/` | One project's worked roadmap and 26-case suite |

## The components

| Layer | Component | Use it to answer |
|---|---|---|
| 0 | contract-runner | Does an adapter behave as specified? |
| 0 | session-export | Which tools did a run call, in order? |
| 1 | langfuse-trace | What are agents doing, and what does it cost? |
| 2 | pairwise-fixtures | Does the parser handle every pair of input variations? |
| 3 | tool-correctness | Did the agent follow the verified procedure? |
| 4 | domain-metric | Is the pipeline's output good by the field's measure? |
| 5 | human-agreement | Do people agree on the label? Is a judge's rate trustworthy? |
| 6 | runtime-guard | Must a tool call be stopped before it happens? |
| 7 | failure-harvest | How do failures become permanent tests? |

## Quick start

Requires Python 3.10 or later. No packages. CI runs 3.10 and 3.13.

```text
git clone https://github.com/MrSnowNB/hermes-integration-kit.git
cd hermes-integration-kit
python skills/integrate/scripts/check_kit.py
```

`check_kit.py` runs the runner's self-tests, the reference suite, a
reference live job, and a scaffold round-trip, and checks that the vault
matches the catalog.

## Use it in a Hermes project

Make the skill available to Hermes, using one of the documented options:

- Add the kit's skill folder to `skills.external_dirs` in
  `~/.hermes/config.yaml`:

  ```yaml
  skills:
    external_dirs:
      - ~/hermes-integration-kit/skills
  ```

- Or copy `skills/integrate/` into the project's `.hermes/skills/` or
  `.agents/skills/`, then trust the project with `hermes skills trust`.

Then, in a Hermes session inside the project:

```text
/integrate add tracing to this project
```

The agent reads the catalog, scaffolds `integrations/<component>/`, and asks
you to approve the Gate before writing code.

## Status

| Part | Evidence |
|---|---|
| Runner, scaffolder, reference adapter, kit check | Ran in CI and on the build host |
| Hermes commands and behaviors cited in the guides | Stated in official docs; not run on a Hermes host by this kit |
| Vendor adapters (Langfuse, DeepEval, allpairspy, TrackEval, sklearn) | Not included. Each project writes its own through the procedure |
| failure-harvest | Design only |

## Rules

- One component per change.
- Gate before code. Expected results before the run.
- Fail-open tools record. Only fail-closed checks gate.
- Only the operator admits a component.
- Credentials, session stores, and model weights stay out. See `DENY.txt`.
