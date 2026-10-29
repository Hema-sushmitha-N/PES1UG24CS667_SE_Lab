# Lab 6: Code and Branch Coverage

**Student:** HEMA SUSHMITHA N, PES1UG24CS667

Application: coffee shop order processing and espresso machine temperature monitoring.
Source: [assigned repository](https://github.com/SETAPESU26/L6_L7_03_coffee_shop_order).
The application and starter test are copied unchanged. Only additional tests,
coverage configuration, reports and supporting documentation were added.

## Results

| Test suite | Passing tests | Statement coverage | Branch outcomes |
|---|---:|---:|---:|
| Original starter | 1 | 26/54 (48.15%) | 14/38 (36.84%) |
| Code coverage suite | 8 | 54/54 (100%) | Not measured in the line-only run |
| Branch coverage suite | 39 | 54/54 (100%) | 38/38 (100%) |

All 48 tests pass together. The branch-enabled report's `Cover` column combines
statement and branch coverage; its initial 43% is not the branch-only percentage.

## Deliverables

- [Consolidated PDF report: summary and both screenshots](Lab_6_Code_and_Branch_Coverage_Report.pdf)
- [Code coverage tests](CodeCoverageTest_coffee_shop_order.py)
- [Branch coverage tests](BranchCoverageTest_coffee_shop_order.py)
- [Code coverage screenshot](reports/line/terminal_screenshot.png)
- [Branch coverage screenshot](reports/branch/terminal_screenshot.png)
- [Code coverage terminal output](reports/line/terminal_output.txt)
- [Branch coverage terminal output](reports/branch/terminal_output.txt)
- [Preparation and explanation guide](LAB_GUIDE.md)
- Initial reports: [line](reports/baseline/terminal_output.txt), [branch](reports/baseline_branch/terminal_output.txt)

The two submission commits separate the line coverage work from the branch
coverage work, with a result screenshot in each.

## Reproduce

From a PowerShell terminal inside `Lab-6`:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe run_lab.py all
.\.venv\Scripts\python.exe -m pytest -q
```

On this computer the environment is already installed. Use `run_lab.py line`
or `run_lab.py branch` for an individual final measurement. Reports measure only
`coffee_shop_order.py`. HTML reports are generated locally and ignored by Git.
