# Lab 7 bug analysis

The completed suite is identical before and after the fixes. Eight properties
use Hypothesis; fixed-value regressions and CLI checks complement generation.

| Area | Input/evidence | Original behavior | Fix / defined behavior |
|---|---|---|---|
| All three functions | Hypothesis minimizes to `None` | `AttributeError` on `.upper()` or `.split()` | Type checks: return `None` for lookup/average, `{}` for modifiers |
| Drink lookup | Generated whitespace-padded known prefix | `KeyError` | Strip whitespace, uppercase first three characters, use dictionary `.get()` |
| Drink lookup | Regression `moc` | Uppercases to `MOC` but menu contains `MOc` | Normalize dictionary key to `MOC`; returns 5.0 |
| Drink lookup | Regression empty/unknown text | `KeyError` | Return `None`; CLI explains invalid/unknown code |
| Average | Empty text, `1,,3`, `one,two` | Unhandled `ValueError` | Validate text; catch conversion errors and return `None` |
| Average | `nan`, `inf`, `1e309`, negative price | Non-finite or invalid monetary result accepted | Require finite, nonnegative floats; reject whole invalid CSV |
| Average | `1e308,1e308` | Intermediate sum overflows to infinity | Normalize by maximum, use `math.fsum`, rescale; result 1e308 |
| Modifiers | Generated empty dictionary round trip gives empty text | Unpacking `ValueError` | Skip segments without a colon; empty input yields `{}` |
| Modifiers | Empty segments, missing separators, empty keys/values | Unpacking errors or invalid pairs | Validate each segment and retain only nonempty pairs |
| Modifiers | Regression `note:extra:hot` | Too many values to unpack | Split only once; preserve `extra:hot` as the value |
| CLI | Unknown code, malformed CSV | Stops on the first exception | Display invalid-input messages and continue processing |
| CLI | EOF | Unhandled `EOFError` | Print safe termination message |

Known valid menu prices and ordinary averages remain supported. Monetary
nonnegativity and tolerant modifier parsing are documented design choices for
inputs whose behavior is unspecified in the handout.

The original average implementation does not actually divide by zero for empty
text: conversion of the empty token raises `ValueError` first. The report records
the observed exception rather than claiming an unobserved divide-by-zero crash.

## Recorded measurements

- Full completed suite on original source: **34 failed, 10 passed**.
- Three starter fuzz properties on original: **3 failed, 41 deselected**.
- Same full completed suite on fixed source: **44 passed**.
- Original CLI with `moc`: exit 1, `KeyError: 'MOC'`.
- Fixed CLI with the same three input lines: exit 0; price 5.0, average 1.5,
  modifiers `{'milk': 'oat', 'syrup': 'vanilla'}`.

`originals/` retains the exact assigned bytes from commit
`2df8501ea39f90dcb7e339510ddd36d02bffda78`. Raw transcripts and stage exit-code
metadata are in `reports/`. Screenshots are genuine console captures.
