#!/usr/bin/env python3
"""Reference adapter: check that a JSON document carries required keys.

It is deliberately small. It shows the full adapter contract that every
integration in this kit follows:

  stdin   one request object (schema_version, case_id, fixture_sha256, input, output_dir)
  stdout  one response envelope (status, summary, reason_codes, metrics, artifacts, next_actions)
  exit    0 pass, 1 block, 2 error. The exit code and status must agree.

Synthetic mode reads input.document. Live mode reads input.path, relative to
the working directory the runner uses (the suite folder).
"""
import json
from pathlib import Path
import sys

EXIT = {"pass": 0, "block": 1, "error": 2}


def respond(request, status, summary, reasons=(), metrics=None, artifacts=(), actions=()):
    print(json.dumps({
        "schema_version": "1",
        "case_id": request.get("case_id", ""),
        "fixture_sha256": request.get("fixture_sha256", ""),
        "status": status,
        "summary": summary,
        "reason_codes": list(reasons),
        "metrics": metrics or {},
        "artifacts": list(artifacts),
        "next_actions": list(actions),
    }))
    return EXIT[status]


def main():
    try:
        request = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return respond({}, "error", "Request was not JSON.", ["BAD_REQUEST"])
    data = request.get("input", {})
    required = data.get("required")
    if not isinstance(required, list) or not required or not all(
            isinstance(key, str) for key in required):
        return respond(request, "error", "No required-key list supplied.", ["BAD_SPEC"])
    try:
        if data.get("mode") == "live":
            document = json.loads(Path(data["path"]).read_text())
        else:
            document = data.get("document")
    except (KeyError, OSError, json.JSONDecodeError):
        return respond(request, "error", "Document could not be read.", ["UNREADABLE"])
    if not isinstance(document, dict):
        return respond(request, "error", "Document is not a JSON object.", ["NOT_OBJECT"])

    missing = sorted(key for key in required if key not in document)
    metrics = {"required": len(required), "present": len(required) - len(missing),
               "missing": len(missing)}
    report = Path(request["output_dir"]) / "missing.json"
    report.write_text(json.dumps({"missing": missing}, indent=2))
    if missing:
        return respond(request, "block", f"{len(missing)} required key(s) missing.",
                       ["MISSING_KEYS"], metrics, ["missing.json"],
                       ["Add the missing keys, then rerun this case."])
    return respond(request, "pass", "All required keys present.", (), metrics,
                   ["missing.json"])


if __name__ == "__main__":
    sys.exit(main())
