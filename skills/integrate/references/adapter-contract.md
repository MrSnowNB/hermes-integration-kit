# Adapter contract

Every integration talks to the runner through one adapter. The adapter wraps
the pinned upstream tool. The runner never calls the tool directly.

## Request (stdin)

```json
{
  "schema_version": "1",
  "case_id": "BLOCK-PLANTED-FAULT",
  "fixture_sha256": "<sha256 of the canonical input>",
  "input": {"mode": "synthetic", "...": "component-specific fields"},
  "output_dir": "/absolute/evidence/run-xxxx/BLOCK-PLANTED-FAULT"
}
```

`input.mode` is `synthetic` for fixtures and `live` for jobs.

## Response (stdout)

```json
{
  "schema_version": "1",
  "case_id": "BLOCK-PLANTED-FAULT",
  "fixture_sha256": "<echo of the request value>",
  "status": "block",
  "summary": "One sentence a person can read.",
  "reason_codes": ["MISSING_KEYS"],
  "metrics": {"missing": 2},
  "artifacts": ["missing.json"],
  "next_actions": ["Add the missing keys, then rerun this case."]
}
```

## Exit codes

| Exit | Status | Meaning |
|---|---|---|
| 0 | `pass` | The tool judged the input and it met the gate. |
| 1 | `block` | The tool judged the input and it failed the gate. |
| 2 | `error` | The tool could not judge the input. |

## Rules the runner enforces

- `case_id` and `fixture_sha256` must echo the request, so a response cannot
  be replayed against a different fixture.
- `status` and the exit code must agree.
- Any non-pass status needs at least one reason code.
- Metrics must be finite. NaN and Infinity are errors.
- Artifacts are relative paths that exist inside `output_dir`.
- Malformed JSON, timeouts, and missing fields are errors, never passes.
- An empty case selection is an error.

## Writing an adapter

1. Copy `templates/adapter.py` (the scaffolder does this).
2. Call the pinned tool with arguments built from `input`.
3. Map the tool's result to pass, block, or error. Map the tool's own crash,
   missing dependency, or unreadable input to error.
4. Write anything a reviewer needs under `output_dir` and list it.
5. Keep secrets, personal data, and raw media out of artifacts.

The working example is `examples/reference/adapters/required_keys.py`.
