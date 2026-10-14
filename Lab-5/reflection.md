# Lab 5: Static Code Analysis: Reflection

**Student:** Hema Sushmitha N (PES1UG24CS667)
**Repository:** L5_03_energy_tariff

## 1. Which issues were the easiest and which were the hardest to fix?

The easiest fixes were the formatting and style ones: removing the unused `sys` import, adding blank lines between functions, converting `%` formatting to f-strings, and adding docstrings. The tools say exactly what is wrong and where, and the fix does not change how the program behaves.

The hardest fixes were the ones that needed a design decision. Replacing `eval()` meant deciding what input the program should accept and what should happen on bad input, so I used `float()` with a `try/except`. Removing the `global` statements meant changing function signatures: `raise_rates` now returns a new list of rates instead of changing module-level variables, and I had to update `main()` to match. Fixing the mutable default argument also needed care to keep the behaviour right.

## 2. Did the tools report any false positives?

I did not find any clear false positives. Every warning pointed to something real, even when it was minor, such as the missing docstrings. Some warnings depend on judgement, though. The `global` warning (W0603) and the Flake8 line-length limit of 79 characters are style preferences more than real bugs, and a team might reasonably configure them differently. Bandit's B307 note suggested `ast.literal_eval`, but for this program `float()` was simpler and safer, because the program only needs a number.

The tools also missed things. None of them noticed that negative units produced a negative bill (-192.50), or that `main()` ran every time the file was imported. I found those by reading the program's output and the code. Static analysis does not replace testing or code review.

## 3. How would I use static analysis in a real development workflow?

I would run the tools automatically instead of by hand. Flake8 and Pylint could run as a pre-commit hook or in the editor, so style problems are caught as I type. Bandit, Pylint and Flake8 could also run in a CI pipeline (for example GitHub Actions) on every pull request, and the build would fail if Bandit finds a Medium or High issue or the Pylint score drops below an agreed threshold. The team would keep a shared configuration file (such as `.pylintrc` and `setup.cfg`) so everyone follows the same rules, and would document any justified exceptions instead of silencing warnings.

## 4. What improvements did I see in code quality, readability and robustness?

- **Security:** removing `eval()` closed a code-injection hole. Bandit went from 1 Medium issue to 0.
- **Robustness:** the program no longer crashes or hides errors silently. It catches specific exceptions, handles invalid numbers, rejects negative readings, and closes files properly with `with`.
- **Correctness:** fixing the mutable default argument stopped data from leaking between calls, and the negative-units check removed a wrong negative bill.
- **Readability and maintainability:** docstrings, f-strings, simpler `if` structure and consistent PEP 8 formatting make the code easier to read. Functions that return values instead of changing globals are also easier to test.
- **Measured result:** Pylint improved from 6.14/10 to 10.00/10, Bandit from 1 issue to 0, and Flake8 from 12 warnings to 0.

Overall, the lab showed me that static analysis catches a lot of problems cheaply, before the code is even run, but it works best together with testing and review.
