#!/usr/bin/env python3
"""Contract-test runner for Hermes toolchain integrations. Adapters are supplied per project."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

EXIT = {"pass": 0, "block": 1, "error": 2}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def lookup(value, path):
    for key in path.split("."):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def check(actual, assertion):
    value = lookup(actual, assertion["path"])
    expected = assertion["value"]
    op = assertion["op"]
    if op == "eq":
        return type(value) is type(expected) and value == expected
    if op == "contains":
        return expected in value
    if op == "not_contains":
        return expected not in value
    if op in ("approx", "ge", "le"):
        if type(value) not in (int, float) or not math.isfinite(value):
            return False
        if op == "approx":
            return math.isclose(value, expected, rel_tol=0,
                                abs_tol=assertion.get("atol", 1e-6))
        return value >= expected if op == "ge" else value <= expected
    raise ValueError("unknown assertion operator")


def validate(response, code, request):
    if not isinstance(response, dict):
        raise ValueError("response must be an object")
    if response.get("schema_version") != "1":
        raise ValueError("unsupported response schema")
    for key in ("case_id", "fixture_sha256"):
        if response.get(key) != request[key]:
            raise ValueError("response binding mismatch")
    if response.get("status") not in EXIT or EXIT[response["status"]] != code:
        raise ValueError("exit/status mismatch")
    for key, kind in (("summary", str), ("reason_codes", list),
                      ("metrics", dict), ("artifacts", list),
                      ("next_actions", list)):
        if not isinstance(response.get(key), kind):
            raise ValueError("missing or invalid response field")
    if not all(isinstance(x, str) for x in response["reason_codes"]):
        raise ValueError("reason codes must be strings")
    if response["status"] != "pass" and not response["reason_codes"]:
        raise ValueError("non-pass requires a reason")
    if not all(isinstance(x, str) for x in response["next_actions"]):
        raise ValueError("next actions must be strings")
    # Also rejects NaN/Infinity nested inside metrics.
    canonical(response)
    root = Path(request["output_dir"]).resolve()
    for name in response["artifacts"]:
        if not isinstance(name, str) or Path(name).is_absolute():
            raise ValueError("artifact paths must be relative")
        artifact = (root / name).resolve()
        if not artifact.is_relative_to(root) or not artifact.is_file():
            raise ValueError("missing or escaping artifact")


def run_case(case, command, root, evidence):
    folder = evidence / case["id"]
    folder.mkdir(parents=True, exist_ok=False)
    request = {
        "schema_version": "1", "case_id": case["id"],
        "fixture_sha256": hashlib.sha256(
            canonical(case["input"]).encode()).hexdigest(),
        "input": case["input"], "output_dir": str(folder.resolve()),
    }
    row = {"case_id": case["id"], "stage": case["stage"]}
    try:
        proc = subprocess.run(command, input=canonical(request), text=True,
                              capture_output=True, cwd=root,
                              timeout=case.get("timeout_s", 60), check=False)
        row["adapter_exit"] = proc.returncode
        # Never copy raw stderr or a malformed response into the evidence report.
        response = json.loads(proc.stdout)
        validate(response, proc.returncode, request)
        result_file = folder / "_adapter-result.json"
        with result_file.open("x") as stream:
            stream.write(json.dumps(response, indent=2, allow_nan=False))
        row["result_file"] = str(result_file.resolve())
        ok = proc.returncode == case["expected_exit"]
        ok = ok and all(check(response, a) for a in case["assertions"])
        row.update(verdict="pass" if ok else "fail",
                   adapter_status=response["status"],
                   adapter_exit=proc.returncode,
                   reason_codes=response["reason_codes"])
    except Exception as exc:
        row.update(verdict="error", error_type=type(exc).__name__)
    return row


def execute(suite, root, evidence, stage=None):
    cases = [c for c in suite["cases"] if stage is None or c["stage"] == stage]
    if not cases:
        raise ValueError("empty selection")
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case IDs")
    results = []
    for case in cases:
        if not case["id"] or any(c not in
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in case["id"]):
            raise ValueError("unsafe case ID")
        if case["expected_exit"] not in (0, 1, 2) or not case["assertions"]:
            raise ValueError("missing expectation")
        if not any(a["path"] == "status" and a["op"] == "eq" and
                   a["value"] in EXIT and EXIT[a["value"]] == case["expected_exit"]
                   for a in case["assertions"]):
            raise ValueError("status expectation missing or inconsistent")
        command = suite["adapters"][case["stage"]]
        if not isinstance(command, list) or not command or not all(
                isinstance(x, str) for x in command):
            raise ValueError("adapter must be an argv list")
        command = [x.replace("{python}", sys.executable).replace("{root}", str(root))
                   for x in command]
        results.append(run_case(case, command, root, evidence))
    code = 2 if any(r["verdict"] == "error" for r in results) else (
        1 if any(r["verdict"] == "fail" for r in results) else 0)
    return code, {"schema_version": "1", "suite_id": suite["suite_id"],
                  "cases": len(results),
                  "passed": sum(r["verdict"] == "pass" for r in results),
                  "results": results}


def stub():
    """Private transport fixture for runner self-tests, not a vendor adapter."""
    request = json.load(sys.stdin)
    control = request["input"]
    if control.get("sleep"):
        time.sleep(2)
    if control.get("raw"):
        print(control["raw"])
        return 0
    response = {"schema_version": "1", "case_id": request["case_id"],
                "fixture_sha256": request["fixture_sha256"],
                "status": "pass", "summary": "Synthetic transport response",
                "reason_codes": [], "metrics": {"score": 1.0},
                "artifacts": [], "next_actions": []}
    response.update(control.get("response", {}))
    if control.get("nonfinite"):
        response["metrics"]["score"] = float("nan")
    print(json.dumps(response))
    return control.get("exit", EXIT.get(response["status"], 0))


class HarnessTests(unittest.TestCase):
    def run_fixture(self, payload=None, expected=0, assertions=None, timeout=5):
        case = {"id": "SELFTEST", "stage": "stub", "input": payload or {},
                "expected_exit": expected, "timeout_s": timeout,
                "assertions": assertions or [
                    {"path": "status", "op": "eq",
                     "value": next(k for k, v in EXIT.items() if v == expected)}]}
        with tempfile.TemporaryDirectory() as temp:
            return run_case(case, [sys.executable, str(Path(__file__).resolve()),
                                  "--stub"], Path.cwd(), Path(temp))

    def test_pass(self):
        self.assertEqual(self.run_fixture()["verdict"], "pass")

    def test_expected_block(self):
        payload = {"response": {"status": "block", "reason_codes": ["DENIED"]}}
        self.assertEqual(self.run_fixture(payload, 1)["verdict"], "pass")

    def test_expected_error(self):
        payload = {"response": {"status": "error", "reason_codes": ["OUTAGE"]}}
        self.assertEqual(self.run_fixture(payload, 2)["verdict"], "pass")

    def test_unexpected_block(self):
        payload = {"response": {"status": "block", "reason_codes": ["DENIED"]}}
        self.assertEqual(self.run_fixture(payload)["verdict"], "fail")

    def test_exit_mismatch(self):
        self.assertEqual(self.run_fixture({"exit": 1})["verdict"], "error")

    def test_bad_json(self):
        self.assertEqual(self.run_fixture({"raw": "not-json"})["verdict"], "error")

    def test_timeout(self):
        self.assertEqual(self.run_fixture({"sleep": True}, timeout=.05)
                         ["verdict"], "error")

    def test_case_binding(self):
        self.assertEqual(self.run_fixture({"response": {"case_id": "OTHER"}})
                         ["verdict"], "error")

    def test_hash_binding(self):
        self.assertEqual(self.run_fixture({"response": {"fixture_sha256": "bad"}})
                         ["verdict"], "error")

    def test_missing_field(self):
        self.assertEqual(self.run_fixture({"response": {"metrics": None}})
                         ["verdict"], "error")

    def test_missing_metric(self):
        checks = [{"path": "metrics.missing", "op": "ge", "value": 0}]
        self.assertEqual(self.run_fixture(assertions=checks)["verdict"], "error")

    def test_numeric_tolerance(self):
        checks = [{"path": "metrics.score", "op": "approx",
                   "value": 1.0000001, "atol": .000001}]
        self.assertEqual(self.run_fixture(assertions=checks)["verdict"], "pass")

    def test_nonfinite_metric(self):
        payload = {"nonfinite": True}
        self.assertEqual(self.run_fixture(payload)["verdict"], "error")

    def test_artifact_escape(self):
        self.assertEqual(self.run_fixture({"response": {
            "artifacts": ["../outside.json"]}})["verdict"], "error")

    def test_missing_artifact(self):
        self.assertEqual(self.run_fixture({"response": {
            "artifacts": ["missing.json"]}})["verdict"], "error")

    def test_numeric_bool_rejected(self):
        self.assertFalse(check({"x": True}, {"path": "x", "op": "ge", "value": 0}))

    def test_empty_selection(self):
        with self.assertRaises(ValueError):
            execute({"cases": []}, Path.cwd(), Path.cwd())

    def test_unknown_operator(self):
        with self.assertRaises(ValueError):
            check({"x": 1}, {"path": "x", "op": "unknown", "value": 1})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", nargs="?")
    parser.add_argument("--stage")
    parser.add_argument("--job", help="Run a live job JSON via the suite's adapter map")
    parser.add_argument("--evidence", default="evidence")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--stub", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.stub:
        return stub()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(HarnessTests))
        return 0 if result.wasSuccessful() else 1
    try:
        if not args.suite:
            raise ValueError("suite required")
        path = Path(args.suite).resolve()
        suite = json.loads(path.read_text())
        if suite.get("schema_version") != "1":
            raise ValueError("unsupported suite schema")
        evidence_root = Path(args.evidence).resolve()
        evidence_root.mkdir(parents=True, exist_ok=True)
        evidence = Path(tempfile.mkdtemp(prefix="run-", dir=evidence_root))
        if args.job:
            if args.stage:
                raise ValueError("--job and --stage are mutually exclusive")
            job_path = Path(args.job).resolve()
            job = json.loads(job_path.read_text())
            if job.get("schema_version") != "1" or job["input"].get("mode") != "live":
                raise ValueError("live job schema required")
            case = {**job, "expected_exit": 0, "assertions": [
                {"path": "status", "op": "eq", "value": "pass"}]}
            job_suite = {**suite, "suite_id": job["id"], "cases": [case]}
            code, report = execute(job_suite, path.parent, evidence)
            row = report["results"][0]
            code = row.get("adapter_exit", 2) if row["verdict"] != "error" else 2
            report["mode"] = "live"
            report["job_sha256"] = hashlib.sha256(job_path.read_bytes()).hexdigest()
        else:
            code, report = execute(suite, path.parent, evidence, args.stage)
            report["mode"] = "synthetic"
        report["suite_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        report["evidence_dir"] = str(evidence)
        (evidence / "results.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        return code
    except Exception as exc:
        print(json.dumps({"status": "error", "error_type": type(exc).__name__}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
