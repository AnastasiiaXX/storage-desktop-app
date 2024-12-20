import pytest
from src.material_calc import MaterialCalculator

def test_valid_input():
    # Пример из задания
    result = MaterialCalculator.calculate_material(15, 20, 45, 3, 1)
    assert result == 114147

def test_invalid_product_type():
    result = MaterialCalculator.calculate_material(10, 10, 10, 99, 1)
    assert result == -1

def test_invalid_material_type():
    result = MaterialCalculator.calculate_material(10, 10, 10, 1, 99)
    assert result == -1

def test_invalid_count():
    result = MaterialCalculator.calculate_material(-5, 10, 10, 1, 1)
    assert result == -1

def test_zero_count():
    result = MaterialCalculator.calculate_material(0, 10, 10, 1, 1)
    assert result == -1

def test_large_input():
    result = MaterialCalculator.calculate_material(1000, 50, 50, 2, 2)
    assert result > 0
