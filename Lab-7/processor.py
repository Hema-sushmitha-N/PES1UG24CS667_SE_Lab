"""Coffee shop input processing hardened using Hypothesis counterexamples.

Invalid drink/price input returns None. Modifier parsing keeps valid pairs,
skips malformed pairs, preserves colons in values, and uses the last duplicate.
"""

import math


def lookup_drink_code(code_string):
    """Return a known prefix price, or None for an unknown/invalid input."""
    if not isinstance(code_string, str):
        return None
    code_prefix = code_string.strip().upper()[:3]
    menu_prices = {
        "LAT": 4.50,
        "CAP": 4.00,
        "ESP": 3.00,
        "AME": 3.50,
        "MOC": 5.00
    }
    return menu_prices.get(code_prefix)

def calculate_average_shot_cost(pricing_csv):
    """Average finite nonnegative prices; reject an invalid CSV as a whole."""
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        return None
    try:
        prices = [float(piece.strip()) for piece in pricing_csv.split(',')]
    except (ValueError, OverflowError):
        return None
    if any(not math.isfinite(price) or price < 0 for price in prices):
        return None
    maximum = max(prices)
    if maximum == 0:
        return 0.0
    # Scaling prevents the intermediate sum overflowing for e.g. 1e308,1e308.
    return maximum * (math.fsum(price / maximum for price in prices) / len(prices))

def parse_order_modifiers(order_spec):
    """Return valid nonempty key:value pairs; ignore malformed segments."""
    modifier_dict = {}
    if not isinstance(order_spec, str):
        return modifier_dict
    items = order_spec.split(';')
    for item in items:
        if ':' not in item:
            continue
        key, value = item.split(':', 1)
        key, value = key.strip(), value.strip()
        if key and value:
            modifier_dict[key] = value
    return modifier_dict

def main():
    try:
        print("==== Running lookup_drink_code ====")
        drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
        price = lookup_drink_code(drink_input)
        if price is None:
            print("Unknown or invalid drink code")
        else:
            print("Base Price: $", price)

        print("\n==== Running calculate_average_shot_cost ====")
        shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
        avg_price = calculate_average_shot_cost(shots_input)
        if avg_price is None:
            print("Invalid shot prices: enter finite nonnegative numbers separated by commas")
        else:
            print("Average Shot Price: $", avg_price)

        print("\n==== Running parse_order_modifiers ====")
        spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
        mods = parse_order_modifiers(spec_input)
        print("Parsed Modifiers:", mods)
    except EOFError:
        print("Input ended; order processing stopped safely")

if __name__ == "__main__":
    main()
