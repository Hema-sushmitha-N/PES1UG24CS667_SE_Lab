"""Energy tariff system: meter readings, tiered billing and spike detection."""
import json
from datetime import datetime

# Global state
meters = {}
RATE_TIER_1 = 3.5
RATE_TIER_2 = 5.0
RATE_TIER_3 = 7.5
SPIKE_LIMIT = 500


def record_reading(meter_id, units, history=None):
    """Store a meter reading and return the reading history."""
    if history is None:
        history = []
    if units < 0:
        raise ValueError("Units cannot be negative")
    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history


def compute_bill(meter_id, tier_rates):
    """Return the tiered bill for a meter."""
    units = meters[meter_id]
    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    return (100 * tier_rates[0] + 200 * tier_rates[1]
            + (units - 300) * tier_rates[2])


def raise_rates(rates, percent):
    """Return a new list of rates increased by the given percent."""
    return [rate * (1 + percent / 100) for rate in rates]


def flag_spikes():
    """Return meters whose usage exceeds the spike limit."""
    spikes = []
    for meter_id, units in meters.items():
        if units > SPIKE_LIMIT:
            spikes.append(meter_id)
    return spikes


def load_meter_data(file="meters.json"):
    """Load meter data from a JSON file, or start empty if unreadable."""
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        data = {}
    meters.clear()
    meters.update(data)


def save_meter_data(file="meters.json"):
    """Save meter data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(meters, f)


def main():
    """Run the energy tariff demo."""
    history = []
    record_reading("M-01", 120, history)
    record_reading("M-02", 640, history)
    record_reading("M-03", 50, history)
    print("Readings stored so far:", len(history))
    rates = raise_rates([RATE_TIER_1, RATE_TIER_2, RATE_TIER_3], 10)
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print("Spikes:", flag_spikes())
    adjustment = input(
        "Extra units for M-01 as an expression (Enter for 0): "
    ) or "0"
    try:
        extra_units = float(adjustment)
    except ValueError:
        print("Invalid number entered, using 0.")
        extra_units = 0.0
    record_reading("M-01", extra_units, history)
    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
