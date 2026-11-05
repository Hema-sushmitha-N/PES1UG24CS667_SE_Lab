# Lab 7: Fuzzing for Input Validation Bugs

**Student:** HEMA SUSHMITHA N, PES1UG24CS667

Assigned source: [coffee shop repository / Lab 7](https://github.com/SETAPESU26/L6_L7_03_coffee_shop_order/tree/main/Lab%207),
commit `2df8501ea39f90dcb7e339510ddd36d02bffda78`.

This lab completes the three starter Hypothesis tests, discovers input-validation
bugs, fixes `processor.py`, and reruns the identical completed test suite. The
unchanged assigned files are retained under `originals/`. Lab 6 is untouched.

## Deliverables

1. [PDF report with all four required screenshots](Lab_7_Fuzz_Testing_Report.pdf)
2. [Fixed application: processor.py](processor.py)
3. [Updated Hypothesis tests: test_processor.py](test_processor.py)

Supporting evidence: [buggy application](reports/buggy_app/),
[failing tests](reports/failing_tests/), [fixed application](reports/fixed_app/),
[passing tests](reports/passing_tests/), and [bug analysis](BUG_ANALYSIS.md).

## Results

| Measurement | Result |
|---|---|
| Original application, input `moc` | Crashes with `KeyError: 'MOC'` |
| Completed suite against original code | 34 failed, 10 passed |
| Fixed application, same inputs | Price 5.0, average 1.5, parsed modifiers |
| Identical suite against fixed code | **44 passed** |
| Three starter fuzz properties against original | 3 failed, 41 deselected |

The failing-test screenshot selects just the three original fuzz properties so
their failures fit legibly on one screen. The complete 44-test baseline output,
including Hypothesis counterexamples and the 34/10 result, is preserved in
`reports/failing_tests/terminal_output.txt`.

There are eight Hypothesis property tests, 33 parametrized regression cases,
and three CLI tests. Hypothesis uses up to 200 generated examples per property,
with deterministic generation and shrinking. A pytest test count is not an
exact count of generated examples; finite strategies can exhaust earlier.

## Run locally

Open `C:\Users\sushm\Desktop\PES1UG24CS667_SE_Lab` in VS Code and use PowerShell:

```powershell
cd 'C:\Users\sushm\Desktop\PES1UG24CS667_SE_Lab\Lab-7'
.\.venv\Scripts\python.exe processor.py
.\.venv\Scripts\python.exe -m pytest test_processor.py -q
```

Python, pytest and Hypothesis are already prepared in `Lab-7/.venv` on this PC.
On another computer, from inside `Lab-7`:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

To reproduce all four stages, including expected original failures:

```powershell
.\.venv\Scripts\python.exe tools\run_evidence.py all
```

The evidence runner checks expected exit codes: 1 for original crashes/failures,
0 for the fixed application and passing tests. It does not turn test failures
into test passes. For a direct before-fix pytest run:

```powershell
$env:LAB7_TARGET = 'original'
.\.venv\Scripts\python.exe -m pytest test_processor.py -q
Remove-Item Env:\LAB7_TARGET
.\.venv\Scripts\python.exe -m pytest test_processor.py -q
```

Actual console screenshots can be recaptured using:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\capture_evidence.ps1
```

The script-policy override is process-only. PDF generation additionally uses
ReportLab; it is not a dependency for running the lab application or tests.

## Input policy used for the fixes

- Drink lookup accepts strings, strips surrounding whitespace and uses the first
  three uppercase characters. Unknown, empty or non-string input returns `None`.
- A shot-price CSV must contain only finite, nonnegative numbers. Empty, malformed,
  non-string, negative or non-finite input returns `None`; valid zero prices return
  `0.0`. An invalid token rejects the whole CSV rather than silently changing it.
- Modifier parsing returns a dictionary. Non-string input produces `{}`. Empty or
  malformed segments and empty keys/values are skipped, valid pairs are preserved,
  colons after the first remain in the value, and the last duplicate key wins.
- The CLI prints clear invalid-input messages and handles end-of-input safely.

The handout does not prescribe return values for invalid inputs. These explicit
policies make the functions safe while retaining valid coffee-shop calculations.

## Explaination

`@given` asks Hypothesis to generate values from strategies such as `st.text()`
and `st.none()`. The three starter properties fail if an unexpected exception
escapes. Hypothesis shrinks a failing input to a smaller counterexample; here
the recorded failures include `None` for all three functions. Additional
properties verify meaningful behavior: known drink prices, correct averages,
finite/bounded results and modifier round trips. Regression tests preserve
specific cases such as `moc`, `1,,3`, `nan`, `1e308,1e308` and `note:extra:hot`.

Fuzz testing differs from Lab 6 coverage: it generates unexpected inputs to
find bugs, and this handout explicitly requires fixing the application.
Passing these tests improves robustness but does not prove safety for every
possible input size or resource-exhaustion scenario.
