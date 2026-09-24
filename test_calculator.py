# test_calculator.py
# Unit tests for the Cloud Cost Estimator calculator module
# Run with: python -m pytest test_calculator.py -v

import pytest
from calculator import calculate_ec2, calculate_s3, total_cost


# ── EC2 Tests ───────────────────────────────────────────────

def test_ec2_free_tier():
    """t2.micro at or under 750 hours should cost $0"""
    result = calculate_ec2(750, "t2.micro")
    assert result["cost"] == 0.0
    assert result["free_tier"] == True


def test_ec2_over_free_tier():
    """t2.micro over 750 hours should have a cost"""
    result = calculate_ec2(800, "t2.micro")
    assert result["cost"] > 0
    assert result["free_tier"] == False


def test_ec2_paid_instance():
    """t2.small is never free tier — cost should match rate"""
    result = calculate_ec2(100, "t2.small")
    assert result["cost"] == round(100 * 0.023, 4)
    assert result["free_tier"] == False


def test_ec2_unknown_instance():
    """Unknown instance type should raise ValueError"""
    with pytest.raises(ValueError):
        calculate_ec2(100, "t99.gigantic")


def test_ec2_zero_hours():
    """Zero hours should produce zero cost"""
    result = calculate_ec2(0, "t2.small")
    assert result["cost"] == 0.0


# ── S3 Tests ────────────────────────────────────────────────

def test_s3_free_tier():
    """Under 5 GB should be free"""
    result = calculate_s3(3)
    assert result["cost"] == 0.0
    assert result["free_tier"] == True


def test_s3_exact_free_tier():
    """Exactly 5 GB should still be free"""
    result = calculate_s3(5)
    assert result["cost"] == 0.0
    assert result["free_tier"] == True


def test_s3_over_free_tier():
    """Over 5 GB should charge for the excess only"""
    result = calculate_s3(10)
    assert result["billable_gb"] == 5
    assert result["cost"] == round(5 * 0.023, 4)


# ── Total Cost Tests ────────────────────────────────────────

def test_total_cost():
    """Total should sum all service costs correctly"""
    results = [
        calculate_ec2(100, "t2.small"),
        calculate_s3(20)
    ]
    expected = round(results[0]["cost"] + results[1]["cost"], 4)
    assert total_cost(results) == expected


def test_total_cost_all_free():
    """All free tier services should total zero"""
    results = [
        calculate_ec2(750, "t2.micro"),
        calculate_s3(5)
    ]
    assert total_cost(results) == 0.0