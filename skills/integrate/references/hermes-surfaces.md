# Hermes surfaces: where a component attaches

Pick the surface by what the component must do. Commands are from the
official Hermes docs linked at the end. Confirm each one on the target host
before writing a tool note.

| Need | Surface | Can it block? | Use when |
|---|---|---|---|
| Record what happened | Plugin with observer hooks (`pre_api_request`, `post_api_request`, `pre_tool_call`, `post_tool_call`) | No. Observers are read-only. | Tracing, metrics, audit, export. |
| Stop a tool call now | Shell hook on `pre_tool_call` with `fail_closed: true` | Yes | A call must never happen. |
| React to gateway events | Gateway hook (`HOOK.yaml` plus `handler.py` under the profile's `hooks/`) | Depends on event | Messaging gateway only. CLI, TUI, Desktop, and cron do not load gateway hooks. |
| Teach a procedure | Skill (`SKILL.md`) | No | Agents should follow steps the same way each time. |
| Run on a schedule | Cron job, with `--skill`, or `--no-agent --script` | Through its own exit code | Nightly summaries, weekly harvest lists. |
| Decide what merges | CI step running the contract runner | Yes, by exit code | Every quality gate. |
| Give the agent a tool | Toolset or MCP server tools | No | The agent needs a new capability, not a check. |

## Commands to know

```text
hermes plugins install langfuse          # per profile; -p <profile> for another
hermes plugins list
hermes sessions export <output> [--session-id ID]
hermes hooks list
hermes hooks test <event> [--for-tool X] [--payload-file F]
hermes hooks doctor
hermes cron create "every 1d at 09:00" "<prompt>" --skill integrate
hermes cron list
hermes cron status
hermes cron doctor
hermes skills trust ~/myproject          # load project skills from a repo
hermes chat --toolsets "web,terminal"
```

## Rules

- A fail-open surface records. It never authorizes. Pair it with a
  fail-closed check if anything depends on it.
- Shell hooks fail open by default: spawn error, timeout, or unparseable
  output logs a warning and the call proceeds. `fail_closed: true` inverts
  that and applies only to `pre_tool_call`.
- Do not query `~/.hermes/state.db` from a gate. Use `hermes sessions export`.
- Plugins, skills, hooks, and cron stores are profile-scoped. Confirm the
  surface in the profile the gateway actually serves.
- Project skills load only from trusted repositories. Cron jobs inherit the
  interactive trust decision for their `workdir`.
- The Langfuse plugin's `sanitized` capture is pattern-based redaction, not a
  data-loss guarantee. Use `metadata` capture for private or minor data.

## Sources

- Hooks: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
- Observer hooks: https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks
- Langfuse plugin: https://hermes-agent.nousresearch.com/docs/plugins/langfuse
- Skills: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Cron: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- CLI reference: https://hermes-agent.nousresearch.com/docs/reference/cli-commands
- Tools and toolsets: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools
