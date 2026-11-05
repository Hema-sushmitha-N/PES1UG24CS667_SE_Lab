"""Save actual before/after application and pytest output without editing results."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STAGES = ("buggy_app", "failing_tests", "fixed_app", "passing_tests")


def run(stage, compact=False):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env.pop("LAB7_TARGET", None)
    stdin = None
    if stage.endswith("app"):
        script = "originals/processor.py" if stage == "buggy_app" else "processor.py"
        command = [sys.executable, script]
        stdin = "moc\n1.0,1.5,2.0\nmilk:oat;syrup:vanilla\n"
    else:
        command = [sys.executable, "-m", "pytest", "test_processor.py", "-q", "--color=no"]
        if stage == "failing_tests":
            env["LAB7_TARGET"] = "original"
        if compact and stage == "failing_tests":
            command += ["-k", "test_lookup_drink_code_no_crash or test_calculate_average_shot_cost_safe or test_parse_order_modifiers_safe", "--tb=no"]
        else:
            command += ["--tb=short"]
    header = [f"Lab 7 | {stage} | HEMA SUSHMITHA N | PES1UG24CS667"]
    if stdin:
        header += ["Inputs (one per prompt): moc | 1.0,1.5,2.0 | milk:oat;syrup:vanilla"]
    if env.get("LAB7_TARGET"):
        header += ["LAB7_TARGET=original (identical completed tests; buggy source)"]
    header += ["> " + subprocess.list2cmdline(command)]
    result = subprocess.run(command, cwd=ROOT, input=stdin, text=True, encoding="utf-8",
                            errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    expected = 1 if stage in ("buggy_app", "failing_tests") else 0
    body = "\n".join(header) + "\n" + result.stdout + f"\nExit code: {result.returncode} (expected {expected})\n"
    print(body, end="")
    if compact:
        destination = ROOT / "reports" / stage
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "compact_terminal_output.txt").write_text(body, encoding="utf-8")
    if not compact:
        destination = ROOT / "reports" / stage
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "terminal_output.txt").write_text(body, encoding="utf-8")
        (destination / "result.json").write_text(json.dumps({"stage": stage, "command": command,
            "returncode": result.returncode, "expected_returncode": expected,
            "target": env.get("LAB7_TARGET", "fixed"), "stdin": stdin}, indent=2), encoding="utf-8")
    if result.returncode != expected:
        raise SystemExit(f"Unexpected exit code for {stage}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=[*STAGES, "all"])
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    for stage in STAGES if args.stage == "all" else [args.stage]:
        run(stage, args.compact)
