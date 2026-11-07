# Agent guidelines

These rules apply to any agent (Hermes, Codex, Claude Code, or other) that
works in this repository or uses the `integrate` skill in another project.

## Integrating a component into a project

Load `skills/integrate/SKILL.md` and follow its Procedure. In short:

1. Read `skills/integrate/references/catalog.json` and the project's
   `integrations/LEDGER.md`. Choose the next component whose `depends_on`
   entries are admitted and whose `use_when` matches the operator's goal.
2. Scaffold it with `skills/integrate/scripts/scaffold.py`.
3. Fill in the Gate. Stop and ask the operator to approve it.
4. After approval, pin and install. Installing requires approval.
5. Write expected results, then fixtures, then the adapter. Run the
   synthetic suite until every case matches, including block and error.
6. Run one live job twice. Save the evidence.
7. Present the Gate, evidence paths, and failures seen. The operator admits.

### Hard rules

- One component per branch and per pull request.
- Never edit a fixture, expected result, or threshold to make a run pass.
  Report the failure instead.
- Never treat a fail-open signal (tracing, default shell hooks) as a gate.
- Never read `~/.hermes/state.db` from a gate. Use `hermes sessions export`.
- Never commit anything matched by `DENY.txt`.
- Never set a ledger row to `admitted` or `retired`.
- Never attach a component to a Hermes surface (plugin, hook, cron, CI)
  without operator approval.
- Label every claim with an evidence label from `vault/SCHEMA.md`. A command
  you have not run on the target host is not `verified-local`.

### Asking the operator

When you need approval, give: the component, the Gate text, the exact
install or attach command, what data it will see, and the rollback step.
Then wait.

## Changing this kit

1. **Catalog first.** Edit `skills/integrate/references/catalog.json`. New
   components start with `evidence: untested` and need at least three
   synthetic cases (pass, block, error) and one sample job.
2. **Render.** Run
   `python skills/integrate/scripts/render_tool_notes.py --catalog skills/integrate/references/catalog.json --out vault/tools`.
3. **Check.** Run `python skills/integrate/scripts/check_kit.py`. It must
   exit 0.
4. **Runner changes** need a matching self-test in `toolchain_harness.py`.
   Keep it standard-library only.
5. **Cite upstream.** Any Hermes or vendor command in a guide links to its
   official documentation.
6. **Prose.** Short sentences. No em dashes. No marketing language.

## Definition of done

- `check_kit.py` exits 0.
- Every new or changed claim carries an evidence label and a source.
- The README Status table still tells the truth.
