from hypothesis import given, strategies as st
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers

@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    # To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    # To-Do:Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    # To-Do:Using try and except complete this function.
    pass