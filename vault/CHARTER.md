---
title: "Hermes Integration Kit"
type: agent-toolbox-charter
status: draft
version: "0.1.0"
created: "2026-11-07"
platform: "any Hermes host: Linux, macOS, Windows"
agent_access:
  read: true
  draft_write: true
  direct_system_changes: false
  privileged_actions_require_approval: true
  external_actions_require_approval: true
source_policy:
  raw_sources_immutable: true
  synthesized_notes_require_provenance: true
  local_observations_timestamped: true
  secrets_permitted: false
secrets: false
evidence: untested
---

# Hermes Integration Kit

## Purpose

This vault is the shared toolset for adding evaluation and control
components to any Hermes project. It holds what each component is for, when
to use it, how it attaches to Hermes, and how it is proven before anyone
trusts it.

The executable parts live in `../skills/integrate/`. Agents load that folder
as the `integrate` skill. People read this vault.

## Operating principle

1. One component at a time. Each one feeds the next.
2. Write the gate before the code. Write expected results before the run.
3. Prove it on synthetic fixtures with a known answer, including a planted
   failure that must be caught.
4. Show it on one real job, twice.
5. The model proposes. The gate and the operator authorize.

## Agent permissions

May, on their own:

- Read the vault and the skill.
- Scaffold an integration in a project branch.
- Write fixtures, adapters, and drafts in that branch.
- Run the contract runner.
- Append a dated gap to `inbox/`.

Ask the operator first, then:

- Install or upgrade any package, plugin, hook, or service.
- Attach a component to a Hermes surface (plugin, hook, cron, CI).
- Write `tools/`, `toolchains/`, `runbooks/`, `decisions/`, or this charter.
- Move a ledger row to `admitted` or `retired`. Only the operator does this.
- Send data off the host.

## Structure

```text
hermes-integration-kit/
├── README.md, START.txt, DENY.txt, AGENTS.md
├── skills/integrate/          # the agent skill: procedure, runner, templates
│   ├── SKILL.md
│   ├── references/            # catalog.json, rollout, adapter contract, surfaces
│   ├── scripts/               # runner, scaffolder, note renderer, kit check
│   ├── templates/             # per-integration skeleton
│   └── examples/reference/    # a working adapter, suite, and job
├── examples/attack-first/     # one project's worked roadmap
└── vault/                     # this toolbox, for people
    ├── tools/                 # one note per catalog component
    ├── toolchains/            # ordered combinations
    ├── foundations/           # when-to-use guide
    ├── inbox/                 # drafts and gaps
    ├── runbooks/              # after a procedure has run
    └── decisions/             # after operator review
```

## Definition of success

An operator can open this vault and answer, for any project:

- Which component comes next, and why.
- What it proves and what it does not.
- Where its synthetic results and live evidence are.
- How to remove it in one step.
