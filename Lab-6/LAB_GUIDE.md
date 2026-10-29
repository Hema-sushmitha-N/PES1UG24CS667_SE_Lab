# Lab 6: Coffee Shop Order - preparation and results

Student: HEMA SUSHMITHA N, PES1UG24CS667.

Your message says the lab is in G08 tomorrow: Friday, 30 October 2026.
The room and date come from your message, not from the handout.

## Ready on this computer

- Project: `C:\Users\sushm\Desktop\PES1UG24CS667_SE_Lab\Lab-6`
- Python 3.14.6: already installed; no additional Python installation needed.
- Git and VS Code: already installed.
- Dedicated environment: `.venv` inside `Lab-6`
- Installed here: pytest 9.2.0 and coverage 7.17.0, with their dependencies.
- No database, web server, Node.js packages, pytest-cov, or other application libraries are needed.
- `coffee_shop_order.py` and the original `test_coffee_shop.py` are unchanged.
- All work for this lab is in the submission repository's `Lab-6` directory.

## Run in a VS Code PowerShell terminal

Open your SE lab repository in VS Code. Choose the Python interpreter
`.venv\Scripts\python.exe` if the Python extension is available. The commands
below also work without that extension or virtual environment activation.

```powershell
cd 'C:\Users\sushm\Desktop\PES1UG24CS667_SE_Lab\Lab-6'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe run_lab.py line
.\.venv\Scripts\python.exe run_lab.py branch
```

Expected: 48 tests pass overall; the line suite has 8 tests and the branch
suite has 39 tests. The starter file contributes the remaining one test.
`run_lab.py` runs the actual coverage commands and saves console output,
JSON and an HTML report under `reports/<stage>/`.
To reproduce all four measurements, run `run_lab.py all`.

These are the direct commands corresponding to the handout. Run them in
order; a new `coverage run` replaces the default measurement:

```powershell
# Original tests: initial line coverage
.\.venv\Scripts\python.exe -m coverage run --source=coffee_shop_order -m pytest test_coffee_shop.py
.\.venv\Scripts\python.exe -m coverage report -m

# Original tests: initial branch coverage
.\.venv\Scripts\python.exe -m coverage run --branch --source=coffee_shop_order -m pytest test_coffee_shop.py
.\.venv\Scripts\python.exe -m coverage report -m

# Improved line coverage
.\.venv\Scripts\python.exe -m coverage run --source=coffee_shop_order -m pytest CodeCoverageTest_coffee_shop_order.py
.\.venv\Scripts\python.exe -m coverage report -m

# Improved branch coverage
.\.venv\Scripts\python.exe -m coverage run --branch --source=coffee_shop_order -m pytest BranchCoverageTest_coffee_shop_order.py
.\.venv\Scripts\python.exe -m coverage report -m
.\.venv\Scripts\python.exe -m coverage html
```

`--source=coffee_shop_order` measures only the application. Measuring the test
files themselves would distort the application's coverage result.
The configuration in `pytest.ini` lets pytest discover the two deliverable
filenames, whose capitalized names are outside pytest's default `test_*.py` pattern.

## Measured results

| Suite | Passing tests | Line coverage | Branch outcomes covered |
|---|---:|---:|---:|
| Original starter | 1 | 26/54 = 48.15% | 14/38 = 36.84% |
| Code coverage deliverable | 8 | 54/54 = 100% | Not measured in its line-only run |
| Branch coverage deliverable | 39 | 54/54 = 100% | 38/38 = 100% |

In a branch-enabled report, coverage's `Cover` column combines statements and
branch outcomes. The starter's displayed 43% is `(26+14)/(54+38)`, not its
branch-only percentage. The final branch suite reaches 100% for both measures.
There are no missing lines or missing measured branch outcomes in that suite.

## What the tests exercise

The line suite reaches the validation exception, all size assignments,
unpaid and invalid-size skips, invalid customizations, syrup, ordinary add-ons,
strict allergy cancellation, membership, all three order statuses, and the
machine's no-data, optimal and shutdown returns.

The branch suite independently covers both outcomes of decisions and adds:

- Wrong orders type and negative tax separately, including the validation's short circuit.
- Empty, unpaid and invalid-size batches; default size and missing customization fields.
- All sizes with and without membership, with expected totals asserted.
- Syrup at 0, below 1.5, exactly 1.5, and above 1.5; the cap is 1.5.
- Negative customization cost skipped while later valid customization still executes.
- Strict and non-strict allergy alerts; strict cancellation stops later customizations
  and affects only that order. Non-strict alert cost is not added.
- Exactly four versus five rejections; audit rejection takes priority even when the total is zero.
- Invalid-size, negative-cost and allergy rejections contributing to the audit count.
- Mixed paid/unpaid orders, discount followed by tax, and final rounding.
- Empty machine input, an empty inner cycle, exactly 96 degrees, values above 96,
  two consecutive hot readings, a normal reading resetting the streak, and
  resetting the streak between cycles.

## Explain it during the lab

- **Line coverage:** Did every executable statement run at least once?
- **Branch coverage:** Did every measured decision outcome run? Executing an `if`
  body does not demonstrate its false outcome. Loops also have branch outcomes.
- **Path coverage:** Did every complete route through the program run? This is
  stronger than branch coverage; loops can create arbitrarily many paths.
- **Function coverage:** Was each function called? Both functions are exercised here.
- `coverage run` executes tests while recording coverage; `--branch` also records
  branch outcomes. `-m pytest` invokes pytest as a module.
- In `coverage report -m`, `-m` means show missing lines. `Stmts` is executable
  statements, `Miss` is missed statements, `Branch` is branch outcomes, and
  `BrPart` is partially covered branch locations.
- `pytest.mark.parametrize` runs the same test with several distinct input and
  expected-output combinations; each combination is reported as a separate test.
- `pytest.raises` checks the validation exception. Output assertions check both
  total and status so the tests verify behavior as well as execution.
- 100% branch coverage does not prove correctness or full condition/path coverage.
  For example, extra cases around the syrup cap test behavior beyond the reported branch count.

## Submission files and screenshots

The handout asks for separate line and branch test files, result screenshots
after reaching at least 90%, and at least two commits. Included files:

- `CodeCoverageTest_coffee_shop_order.py`
- `BranchCoverageTest_coffee_shop_order.py`
- `reports/line/terminal_screenshot.png`
- `reports/branch/terminal_screenshot.png`
- `reports/line/terminal_output.txt` and `reports/branch/terminal_output.txt`
- JSON measurements; initial reports for comparison (no initial screenshots).

Screenshots are actual captures of Windows console windows running these tests,
not illustrations. `show_evidence.ps1` displays results; `capture_evidence.ps1`
can recapture the two consoles. Its script-policy override is process-only:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\capture_evidence.ps1
```

The two local commits separate the line coverage deliverable from the branch
coverage deliverable. To inspect them and confirm the original code is unchanged:

```powershell
git log -2 --oneline
git status --short --branch
```

The submission repository is `Hema-sushmitha-N/PES1UG24CS667_SE_Lab`, and this
lab belongs in its `Lab-6` folder alongside the previous labs. Both original
Python files match the assigned repository byte for byte.

## Recreate on another computer

Install Python 3.x, Git and an editor first. For the tested versions here,
use Python 3.14; the pinned pytest requires a supported modern Python version.
Clone your submission repository, enter `Lab-6`, then run:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe run_lab.py all
```

Once dependencies are installed and the repository is local, tests and coverage
run without internet. The environment folder is intentionally not committed.
