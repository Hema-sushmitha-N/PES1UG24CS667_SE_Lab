"""Independent branch suite, including boundaries and observable calculations."""

import pytest

from coffee_shop_order import check_espresso_machine, process_order_batch


@pytest.mark.parametrize("orders,tax", [(None, 0), ({}, 0), ((), 0), ([], -0.01)])
def test_invalid_input(orders, tax):
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch(orders, tax)


@pytest.mark.parametrize("orders", [[], [{}], [{"paid": False}], [{"paid": True, "size": "unknown"}]])
def test_no_sale(orders):
    assert process_order_batch(orders, 0.1) == {"total": 0.0, "status": "NO_SALE"}


@pytest.mark.parametrize("size,price", [("small", 3.0), ("medium", 4.5), ("large", 6.0)])
@pytest.mark.parametrize("member", [False, True])
def test_sizes_membership_and_tax(size, price, member):
    result = process_order_batch([{"paid": True, "size": size, "is_member": member}], 0.1)
    expected = round(price * (0.9 if member else 1) * 1.1, 2)
    assert result == {"total": expected, "status": "COMPLETED"}


def test_defaults_for_size_modification_type_and_cost():
    orders = [{"paid": True, "customizations": [{}, {"cost": 0.5}]}]
    assert process_order_batch(orders, 0) == {"total": 5.0, "status": "COMPLETED"}


@pytest.mark.parametrize("cost,added", [(0, 0), (1.49, 1.49), (1.5, 1.5), (1.51, 1.5), (5, 1.5)])
def test_syrup_cap(cost, added):
    orders = [{"paid": True, "customizations": [{"type": "syrup", "cost": cost}]}]
    assert process_order_batch(orders, 0) == {"total": round(4.5 + added, 2), "status": "COMPLETED"}


def test_negative_cost_is_skipped_and_next_customization_runs():
    orders = [{"paid": True, "customizations": [
        {"type": "milk", "cost": -0.01},
        {"type": "milk", "cost": 0.5},
    ]}]
    assert process_order_batch(orders, 0) == {"total": 5.0, "status": "COMPLETED"}


@pytest.mark.parametrize("strict,expected_total,expected_status", [
    (False, 5.0, "COMPLETED"), (True, 0.0, "NO_SALE"),
])
def test_allergen_strict_cancels_item_and_stops_customizations(strict, expected_total, expected_status):
    orders = [{"paid": True, "strict_allergy": strict, "customizations": [
        {"type": "milk", "cost": 0.25},
        {"type": "allergen_alert", "cost": 10},
        {"type": "milk", "cost": 0.25},
    ]}]
    # Non-strict alerts count as rejections but their cost is not added.
    assert process_order_batch(orders, 0) == {"total": expected_total, "status": expected_status}


def test_strict_allergy_cancels_only_its_own_order():
    orders = [
        {"paid": True, "strict_allergy": True, "customizations": [{"type": "allergen_alert"}]},
        {"paid": True, "size": "small"},
    ]
    assert process_order_batch(orders, 0) == {"total": 3.0, "status": "COMPLETED"}


@pytest.mark.parametrize("rejections,paid_sale,status", [
    (4, False, "NO_SALE"), (5, False, "AUDIT_REJECTED"),
    (4, True, "COMPLETED"), (5, True, "AUDIT_REJECTED"),
])
def test_audit_threshold_and_priority(rejections, paid_sale, status):
    orders = [{"paid": True, "size": "invalid"} for _ in range(rejections)]
    if paid_sale:
        orders.append({"paid": True, "size": "small"})
    assert process_order_batch(orders, 0) == {"total": 3.0 if paid_sale else 0.0, "status": status}


@pytest.mark.parametrize("modification", [
    {"type": "milk", "cost": -1}, {"type": "allergen_alert"},
])
def test_customization_rejections_also_count_toward_audit(modification):
    orders = [{"paid": True, "customizations": [dict(modification) for _ in range(5)]}]
    assert process_order_batch(orders, 0) == {"total": 4.5, "status": "AUDIT_REJECTED"}


def test_mixed_batch_skips_unpaid_order_and_applies_tax_after_discount():
    orders = [
        {"paid": False, "size": "large", "customizations": [{"cost": 100}]},
        {"paid": True, "size": "small", "is_member": True,
         "customizations": [{"type": "milk", "cost": 0.5}]},
        {"paid": True, "size": "large"},
    ]
    # (3.5 * 0.9 + 6) * 1.1 = 10.065, rounded using the application's round().
    assert process_order_batch(orders, 0.1) == {"total": round((3.5 * 0.9 + 6) * 1.1, 2), "status": "COMPLETED"}


@pytest.mark.parametrize("cycles,expected", [
    ([], "NO_DATA"),
    ([[]], "OPTIMAL"),
    ([[95, 96, 96]], "OPTIMAL"),
    ([[96.01]], "OPTIMAL"),
    ([[96.01, 96.02]], "SHUTDOWN"),
    ([[97, 96, 98]], "OPTIMAL"),
    ([[97], [98]], "OPTIMAL"),
    ([[], [97, 98], [90]], "SHUTDOWN"),
])
def test_machine_branches_and_temperature_boundary(cycles, expected):
    assert check_espresso_machine(cycles) == expected
