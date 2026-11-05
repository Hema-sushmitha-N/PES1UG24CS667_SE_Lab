"""Run identical properties against the original and fixed processor.

Set LAB7_TARGET=original to reproduce bugs; the default tests processor.py.
"""

import importlib.util
import math
import os
from pathlib import Path

from hypothesis import given, settings, strategies as st
import pytest


if os.environ.get("LAB7_TARGET") == "original":
    spec = importlib.util.spec_from_file_location("original_processor", Path(__file__).parent / "originals" / "processor.py")
    processor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(processor)
else:
    import processor

lookup_drink_code = processor.lookup_drink_code
calculate_average_shot_cost = processor.calculate_average_shot_cost
parse_order_modifiers = processor.parse_order_modifiers

# Reproducible generation and shrinking; no saved examples influence the run.
settings.register_profile("lab7", max_examples=200, deadline=None,
                          derandomize=True, database=None, report_multiple_bugs=False)
settings.load_profile("lab7")


@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    try:
        result = lookup_drink_code(s)
    except Exception as error:
        pytest.fail(f"lookup_drink_code({s!r}) raised {type(error).__name__}: {error}")
    assert result is None or result in (3.0, 3.5, 4.0, 4.5, 5.0)


@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    try:
        result = calculate_average_shot_cost(s)
    except Exception as error:
        pytest.fail(f"calculate_average_shot_cost({s!r}) raised {type(error).__name__}: {error}")
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    try:
        result = parse_order_modifiers(s)
    except Exception as error:
        pytest.fail(f"parse_order_modifiers({s!r}) raised {type(error).__name__}: {error}")
    assert isinstance(result, dict)
    assert all(isinstance(k, str) and k and isinstance(v, str) and v for k, v in result.items())


@given(st.one_of(st.integers(), st.floats(allow_nan=True, allow_infinity=True),
                 st.booleans(), st.lists(st.integers(), max_size=5),
                 st.dictionaries(st.text(max_size=5), st.integers(), max_size=5)))
def test_wrong_types_have_safe_results(value):
    assert lookup_drink_code(value) is None
    assert calculate_average_shot_cost(value) is None
    assert parse_order_modifiers(value) == {}


@given(st.sampled_from([("LAT", 4.5), ("CAP", 4.0), ("ESP", 3.0), ("AME", 3.5), ("MOC", 5.0)]),
       st.sampled_from([str.lower, str.upper, str.title]), st.text(max_size=15))
def test_known_drink_prefixes_ignore_case_and_allow_suffix(pair, case, suffix):
    code, price = pair
    assert lookup_drink_code(" \t" + case(code) + suffix + " \n") == price


@given(st.lists(st.integers(min_value=0, max_value=1_000_000), min_size=1, max_size=30))
def test_valid_csv_average_matches_arithmetic_mean(prices):
    csv = ",".join(f" {price} " for price in prices)
    actual = calculate_average_shot_cost(csv)
    assert actual == pytest.approx(sum(prices) / len(prices))
    assert min(prices) <= actual <= max(prices)


@given(st.lists(st.floats(min_value=0, max_value=1e300, allow_nan=False, allow_infinity=False),
                min_size=1, max_size=20))
def test_finite_prices_produce_finite_bounded_mean(prices):
    result = calculate_average_shot_cost(",".join(map(repr, prices)))
    assert result is not None and math.isfinite(result)
    assert min(prices) * (1 - 1e-14) <= result <= max(prices) * (1 + 1e-14)


token = st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789", min_size=1, max_size=12)


@given(st.dictionaries(token, token, max_size=15))
def test_valid_modifiers_round_trip(modifiers):
    text = ";".join(f" {key} : {value} " for key, value in modifiers.items())
    assert parse_order_modifiers(text) == modifiers


@pytest.mark.parametrize("code,expected", [
    (None, None), ("", None), ("unknown", None), ("  lat  ", 4.5),
    ("cappuccino", 4.0), ("ESP", 3.0), ("ame", 3.5), ("moc", 5.0),
])
def test_drink_regressions(code, expected):
    assert lookup_drink_code(code) == expected


@pytest.mark.parametrize("csv,expected", [
    (None, None), ("", None), ("   ", None), ("1,,3", None),
    (",", None), ("one,two", None), ("nan", None), ("inf", None),
    ("-inf", None), ("1e309", None), ("-1,2", None), ("0,0", 0.0),
    ("1, 2, 3", 2.0), ("1.0, 1.5, 2.0", 1.5),
    ("1e308,1e308", 1e308),
    ("1.7976931348623157e308,1.7976931348623157e308", 1.7976931348623157e308),
])
def test_average_regressions(csv, expected):
    actual = calculate_average_shot_cost(csv)
    if expected is None:
        assert actual is None
    else:
        assert actual == pytest.approx(expected)


@pytest.mark.parametrize("spec,expected", [
    (None, {}), ("", {}), (";", {}), ("milk", {}),
    (":oat;milk:", {}), ("milk:oat;syrup:vanilla", {"milk": "oat", "syrup": "vanilla"}),
    (" milk : oat ;bad; ;syrup:vanilla;", {"milk": "oat", "syrup": "vanilla"}),
    ("note:extra:hot", {"note": "extra:hot"}),
    ("milk:oat;milk:soy", {"milk": "soy"}),
])
def test_modifier_regressions(spec, expected):
    assert parse_order_modifiers(spec) == expected


def test_cli_valid_input(monkeypatch, capsys):
    answers = iter(["moc", "1.0,1.5,2.0", "milk:oat;syrup:vanilla"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    processor.main()
    output = capsys.readouterr().out
    assert "5.0" in output and "1.5" in output and "oat" in output


def test_cli_invalid_input(monkeypatch, capsys):
    answers = iter(["unknown", "1,,3", "bad;milk:oat;"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    processor.main()
    output = capsys.readouterr().out
    assert "Unknown or invalid drink code" in output
    assert "Invalid shot prices" in output
    assert "oat" in output


def test_cli_end_of_input(monkeypatch, capsys):
    def ended(prompt):
        raise EOFError
    monkeypatch.setattr("builtins.input", ended)
    processor.main()
    assert "Input ended" in capsys.readouterr().out
