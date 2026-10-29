"""Run reproducible lab measurements using this environment's Python."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
STAGES = {
    "baseline": ("test_coffee_shop.py", False),
    "baseline_branch": ("test_coffee_shop.py", True),
    "line": ("CodeCoverageTest_coffee_shop_order.py", False),
    "branch": ("BranchCoverageTest_coffee_shop_order.py", True),
}


def run_stage(stage):
    test_file, branch = STAGES[stage]
    output_dir = ROOT / "reports" / stage
    output_dir.mkdir(parents=True, exist_ok=True)
    data_file = output_dir / ".coverage"
    prefix = [sys.executable, "-m", "coverage"]
    commands = [
        prefix + ["run", f"--data-file={data_file}", "--source=coffee_shop_order"]
        + (["--branch"] if branch else [])
        + ["-m", "pytest", test_file, "-v", "--color=no"],
        prefix + ["report", f"--data-file={data_file}", "-m"],
        prefix + ["json", f"--data-file={data_file}", "-o", str(output_dir / "coverage.json")],
        prefix + ["html", f"--data-file={data_file}", "-d", str(output_dir / "html")],
    ]
    transcript = [f"Coffee shop lab: {stage}", f"Working directory: {ROOT}", ""]
    for command in commands:
        transcript.append("> " + subprocess.list2cmdline(command))
        result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        transcript.append(result.stdout.rstrip())
        transcript.append("")
        if result.returncode:
            print("\n".join(transcript))
            raise SystemExit(result.returncode)
    totals = json.loads((output_dir / "coverage.json").read_text())["totals"]
    transcript.append(f"Line coverage: {totals['covered_lines']}/{totals['num_statements']} statements")
    if branch:
        transcript.append(f"Branch coverage: {totals['covered_branches']}/{totals['num_branches']} branch outcomes")
    text = "\n".join(transcript) + "\n"
    (output_dir / "terminal_output.txt").write_text(text, encoding="utf-8")
    print(text)
    if stage in ("line", "branch"):
        assert totals["covered_lines"] == totals["num_statements"], totals
        if branch:
            assert totals["covered_branches"] == totals["num_branches"], totals


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=[*STAGES, "all"])
    args = parser.parse_args()
    for selected in STAGES if args.stage == "all" else [args.stage]:
        run_stage(selected)
