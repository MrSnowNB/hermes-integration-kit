#!/usr/bin/env python3
"""Adapter for {{component}}: {{purpose}}

Contract: read one request object on stdin, print one response envelope on
stdout, exit 0 (pass), 1 (block), or 2 (error). Status and exit must agree.
See skills/integrate/references/adapter-contract.md.

This skeleton fails closed until it is implemented.
"""
import json
import sys


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
    return {"pass": 0, "block": 1, "error": 2}[status]


def main():
    request = json.load(sys.stdin)
    data = request["input"]
    # TODO: call the pinned upstream tool here. Synthetic mode reads fixtures
    # from `data`; live mode reads real inputs named in `data`. Write any
    # evidence files under request["output_dir"] and list them in artifacts.
    return respond(request, "error", "Adapter not implemented.",
                   ["NOT_IMPLEMENTED"], actions=["Implement wrapper/adapter.py"])


if __name__ == "__main__":
    sys.exit(main())
