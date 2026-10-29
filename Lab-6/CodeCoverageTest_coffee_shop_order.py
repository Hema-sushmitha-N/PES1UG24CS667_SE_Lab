"""Line coverage tests: execute every statement in the unchanged application."""

import pytest

from coffee_shop_order import check_espresso_machine, process_order_batch


def test_invalid_orders():
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch(None, 0.1)


def test_sizes_skipped_orders_and_member_discount():
    orders = [
        {"paid": False},
        {"paid": True, "size": "small", "is_member": True},
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large"},
        {"paid": True, "size": "invalid"},
    ]
    # (3 * 0.9 + 4.5 + 6) * 1.1 = 14.52
    assert process_order_batch(orders, 0.1) == {"total": 14.52, "status": "COMPLETED"}


def test_customizations_and_strict_allergy():
    orders = [
        {"paid": True, "customizations": [
            {"type": "standard", "cost": -1},
            {"type": "syrup", "cost": 1},
            {"type": "milk", "cost": 0.5},
        ]},
        {"paid": True, "strict_allergy": True, "customizations": [
            {"type": "allergen_alert", "cost": 0},
        ]},
    ]
    assert process_order_batch(orders, 0) == {"total": 6.0, "status": "COMPLETED"}


def test_five_rejections_trigger_audit():
    orders = [{"paid": True, "size": "invalid"} for _ in range(5)]
    assert process_order_batch(orders, 0) == {"total": 0.0, "status": "AUDIT_REJECTED"}


def test_empty_batch_has_no_sale():
    assert process_order_batch([], 0) == {"total": 0.0, "status": "NO_SALE"}


def test_machine_without_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_machine_recovers_from_one_hot_reading():
    assert check_espresso_machine([[97, 96, 94]]) == "OPTIMAL"


def test_machine_shuts_down_after_two_hot_readings():
    assert check_espresso_machine([[97, 98]]) == "SHUTDOWN"
