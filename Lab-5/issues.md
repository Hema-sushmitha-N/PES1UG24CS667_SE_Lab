# Lab 5: Static Code Analysis: Issues Report

**Student:** Hema Sushmitha N (PES1UG24CS667)
**Repository:** L5_03_energy_tariff
**File analysed:** `energy_system.py`
**Tools:** Pylint, Bandit, Flake8

## Summary of results

| Tool | Before | After |
|---|---|---|
| Pylint score | 6.14 / 10 (22 messages) | 10.00 / 10 |
| Bandit | 1 issue (Medium severity, High confidence) | 0 issues |
| Flake8 | 12 warnings | 0 warnings |

## Issues identified and fixed

Line numbers refer to the **original** file, before the fixes.

| # | Issue | Type | Line(s) | Tool / Code | Description | Fix approach |
|---|---|---|---|---|---|---|
| 1 | Use of `eval()` on user input | Security (Medium) | 63 | Bandit B307, Pylint W0123 | `eval(adjustment)` executes whatever the user types, so arbitrary code could run (CWE-78) | Replaced with `float(adjustment)` inside `try/except ValueError`, falling back to 0 on invalid input |
| 2 | Mutable default argument | Bug | 12 | Pylint W0102 | `history=[]` is created once and shared across every call, so history leaks between calls | Default changed to `None` and a new list created inside the function; `main()` now creates its own `history` list and passes it to each call, so the reading count stays correct |
| 3 | Bare `except:` | Bug / Style | 44 | Pylint W0702, Flake8 E722 | Catches every exception, including `KeyboardInterrupt`, and hides real errors | Catch only `(OSError, json.JSONDecodeError)` |
| 4 | File opened without `with` and without encoding | Resource leak | 42, 48 | Pylint R1732, W1514 | Files were opened and closed manually; the file stays open if an error occurs; encoding was not specified | Used `with open(..., encoding="utf-8")` and `json.load` / `json.dump` |
| 5 | Unused import | Style | 2 | Pylint W0611, Flake8 F401 | `sys` was imported but never used | Removed the import |
| 6 | Missing docstrings | Style | 1, 12, 17, 26, 32, 39, 47, 52 | Pylint C0114, C0116 | Module and all functions had no documentation | Added a module docstring and a docstring for every function |
| 7 | Use of `global` statement | Design | 27, 40 | Pylint W0603 | Functions modified module-level variables through `global`, which hides side effects | `raise_rates` now takes rates and returns a new list; `load_meter_data` uses `meters.clear()` and `meters.update()` |
| 8 | Unnecessary `elif` after `return` | Style | 19 | Pylint R1705 | The `elif` / `else` branches after `return` add needless nesting | Changed to plain `if` statements |
| 9 | Old-style string formatting | Style | 59, 60, 66 | Pylint C0209 | `%` formatting used instead of f-strings | Converted to f-strings |
| 10 | Missing blank lines (7 functions) | Formatting | 12, 17, 26, 32, 39, 47, 52 | Flake8 E302 | PEP 8 requires 2 blank lines before a top-level function | Added a second blank line before each function |
| 11 | Missing blank lines after function | Formatting | 68 | Flake8 E305 | PEP 8 requires 2 blank lines before the code that follows a function | Added a second blank line |
| 12 | Lines too long | Formatting | 24, 62 | Flake8 E501 | Lines longer than 79 characters | Wrapped the expression in `compute_bill` and split the `input(...)` call |
| 13 | Negative units accepted (extra, found manually) | Logic bug | 55 | Not reported by a tool | `record_reading("M-03", -50)` produced a negative bill of -192.50 | `record_reading` now raises `ValueError` for negative units; the demo uses a valid value (50) |
| 14 | `main()` runs on import (extra) | Design | 68 | Not reported by a tool | The script ran its demo whenever the module was imported | Wrapped the call in `if __name__ == "__main__":` |

## Commits

| Commit | Message | Purpose |
|---|---|---|
| `7b3c23c` | Fix Bandit B307: remove eval on user input | Security fix (Bandit) |
| `6f5700c` | Fix Pylint issues, score above 9.5 | Code quality fixes (Pylint) |
| `a30e85f` | Fix Flake8 style issues | PEP 8 formatting (Flake8) |
| `a9c885a` | Add after reports | After reports for all three tools |

## Reports included in this repository

- `pylint_report_before.txt`, `pylint_report_after.txt`
- `bandit_report_before.txt`, `bandit_report_after.txt`
- `flake8_report_before.txt`, `flake8_report_after.txt`
