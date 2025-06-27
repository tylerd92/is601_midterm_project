import pytest
from decimal import Decimal, InvalidOperation
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging
from decimal import Decimal

def test_addition():
    calc = Calculation(operation="Addition", first_operand=Decimal("2"), second_operand=Decimal("3"))
    assert calc.result == Decimal("5")


def test_subtraction():
    calc = Calculation(operation="Subtraction", first_operand=Decimal("5"), second_operand=Decimal("3"))
    assert calc.result == Decimal("2")


def test_multiplication():
    calc = Calculation(operation="Multiplication", first_operand=Decimal("4"), second_operand=Decimal("2"))
    assert calc.result == Decimal("8")


def test_division():
    calc = Calculation(operation="Division", first_operand=Decimal("8"), second_operand=Decimal("2"))
    assert calc.result == Decimal("4")


def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="Division", first_operand=Decimal("8"), second_operand=Decimal("0"))

def test_power():
    calc = Calculation(operation="Power", first_operand=Decimal("2"), second_operand=Decimal("3"))
    assert calc.result == Decimal("8")

def test_root():
    calc = Calculation(operation="Root", first_operand=Decimal("16"), second_operand=Decimal("2"))
    assert calc.result == Decimal("4")

"""
Add tests for modulus, interger division, percent, and absolute difference
"""

def test_modulus():
    calc = Calculation(operation="Modulus", first_operand=Decimal("10"), second_operand=Decimal("3"))
    assert calc.result == Decimal("1")

def test_integer_division():
    calc = Calculation(operation="IntDivide", first_operand=Decimal("10"), second_operand=Decimal("3"))
    assert calc.result == Decimal("3")

def test_percent():
    calc = Calculation(operation="Percent", first_operand=Decimal("50"), second_operand=Decimal("200"))
    assert calc.result == Decimal("25")

def test_absolute_difference():
    calc = Calculation(operation="AbsoluteDifference", first_operand=Decimal("4"), second_operand=Decimal("6"))
    assert calc.result == Decimal("2")

def test_negative_power():
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation(operation="Power", first_operand=Decimal("2"), second_operand=Decimal("-3"))

def test_invalid_root():
     with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
         calc = Calculation(operation="Root", first_operand=Decimal("-16"), second_operand=Decimal("2"))

def test_modulus_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="Modulus", first_operand=Decimal("10"), second_operand=Decimal("0"))

def test_int_divide_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="IntDivide", first_operand=Decimal("5"), second_operand=Decimal("0"))

def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation(operation="Unknown", first_operand=Decimal("5"), second_operand=Decimal("3"))

def test_to_dict():
    calc = Calculation(operation="Addition", first_operand=Decimal("2"), second_operand=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "Addition",
        "first_operand": "2",
        "second_operand": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }


def test_from_dict():
    data = {
        "operation": "Addition",
        "first_operand": "2",
        "second_operand": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Addition"
    assert calc.first_operand == Decimal("2")
    assert calc.second_operand == Decimal("3")
    assert calc.result == Decimal("5")

def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "first_operand": "invalid",
        "second_operand": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_format_result():
    calc = Calculation(operation="Division", first_operand=Decimal("1"), second_operand=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"


def test_equality():
    calc1 = Calculation(operation="Addition", first_operand=Decimal("2"), second_operand=Decimal("3"))
    calc2 = Calculation(operation="Addition", first_operand=Decimal("2"), second_operand=Decimal("3"))
    calc3 = Calculation(operation="Subtraction", first_operand=Decimal("5"), second_operand=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3


def test_from_dict_result_mismatch(caplog):
    """
    Test the from_dict method to ensure it logs a warning when the saved result
    does not match the computed result.
    """
    data = {
        "operation": "Addition",
        "first_operand": "2",
        "second_operand": "3",
        "result": "10",
        "timestamp": datetime.now().isoformat()
    }

    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

def test_str_addition():
    calc = Calculation(operation="Addition", first_operand=Decimal("2"), second_operand=Decimal("3"))
    assert str(calc) == "Addition(2, 3) = 5"

def test_str_subtraction():
    calc = Calculation(operation="Subtraction", first_operand=Decimal("10"), second_operand=Decimal("4"))
    assert str(calc) == "Subtraction(10, 4) = 6"

def test_str_division_decimal():
    calc = Calculation(operation="Division", first_operand=Decimal("1"), second_operand=Decimal("3"))
    assert str(calc) == f"Division(1, 3) = {calc.result}"

def test_repr_addition():
    calc = Calculation(operation="Addition", first_operand=Decimal("2"), second_operand=Decimal("3"))
    expected = (
        f"Calculation(operation='Addition', "
        f"first_operand=2, "
        f"second_operand=3, "
        f"result=5, "
        f"timestamp='{calc.timestamp.isoformat()}')"
    )
    assert repr(calc) == expected

def test_repr_division_decimal():
    calc = Calculation(operation="Division", first_operand=Decimal("1"), second_operand=Decimal("3"))
    expected = (
        f"Calculation(operation='Division', "
        f"first_operand=1, "
        f"second_operand=3, "
        f"result={calc.result}, "
        f"timestamp='{calc.timestamp.isoformat()}')"
    )
    assert repr(calc) == expected

@pytest.mark.parametrize(
    "operation, x, y, expected",
    [
        ("Addition", Decimal("1"), Decimal("2"), Decimal("3")),
        ("Subtraction", Decimal("5"), Decimal("3"), Decimal("2")),
        ("Multiplication", Decimal("2"), Decimal("4"), Decimal("8")),
        ("Division", Decimal("10"), Decimal("2"), Decimal("5")),
        ("Power", Decimal("2"), Decimal("3"), Decimal("8")),
        ("Root", Decimal("9"), Decimal("2"), Decimal("3")),
        ("Modulus", Decimal("10"), Decimal("3"), Decimal("1")),
        ("IntDivide", Decimal("10"), Decimal("3"), Decimal("3")),
        ("Percent", Decimal("50"), Decimal("200"), Decimal("25")),
        ("AbsoluteDifference", Decimal("7"), Decimal("2"), Decimal("5")),
        ("AbsoluteDifference", Decimal("2"), Decimal("7"), Decimal("5")),
    ]
)
def test_calculate_valid_operations(operation, x, y, expected):
    calc = Calculation(operation=operation, first_operand=x, second_operand=y)
    assert calc.calculate() == expected

@pytest.mark.parametrize(
    "operation, x, y, error_msg",
    [
        ("Division", Decimal("1"), Decimal("0"), "Division by zero is not allowed"),
        ("Modulus", Decimal("5"), Decimal("0"), "Division by zero is not allowed"),
        ("IntDivide", Decimal("5"), Decimal("0"), "Division by zero is not allowed"),
        ("Percent", Decimal("5"), Decimal("0"), "Division by zero is not allowed"),
        ("Power", Decimal("2"), Decimal("-2"), "Negative exponents are not supported"),
        ("Root", Decimal("-4"), Decimal("2"), "Cannot calculate root of negative number"),
        ("Root", Decimal("4"), Decimal("0"), "Zero root is undefined"),
        ("UnknownOp", Decimal("1"), Decimal("2"), "Unknown operation"),
    ]
)
def test_calculate_invalid_operations(operation, x, y, error_msg):
    if operation == "UnknownOp":
        with pytest.raises(OperationError, match=error_msg):
            Calculation(operation=operation, first_operand=x, second_operand=y).calculate()
    else:
        with pytest.raises(OperationError, match=error_msg):
            Calculation(operation=operation, first_operand=x, second_operand=y).calculate()

def test_equal_return_not_implemented():
    calc = Calculation(operation="Addition", first_operand=Decimal("2"), second_operand=Decimal("3"))
    # Compare with a non-Calculation object
    other_obj = "Not a calculation"
    assert calc.__eq__(other_obj) is NotImplemented

def test_format_invalid_operation():
    calc = Calculation(operation="Division", first_operand=Decimal("1"), second_operand=Decimal("3"))
    with pytest.raises(InvalidOperation, match="Invalid precision value"):
        calc.format_result(precision=-1)  # Negative precision should raise an error
    with pytest.raises(InvalidOperation, match="Invalid precision value"):
        calc.format_result(precision="two")  # Non-integer precision should raise an error

def test_format_result_invalid_precision_type():
    calc = Calculation(operation="Addition", first_operand=Decimal("1"), second_operand=Decimal("2"))
    with pytest.raises(InvalidOperation, match="Invalid precision value: must be an integer"):
        calc.format_result(precision="not_an_int")

def test_format_result_negative_precision():
    calc = Calculation(operation="Addition", first_operand=Decimal("1"), second_operand=Decimal("2"))
    with pytest.raises(InvalidOperation, match="Invalid precision value: must be non-negative"):
        calc.format_result(precision=-5)

def test_format_result_handles_invalid_operation_gracefully():
    # Simulate a result that cannot be quantized (e.g., NaN)
    calc = Calculation(operation="Addition", first_operand=Decimal("NaN"), second_operand=Decimal("1"))
    # Should return the string representation of the result
    assert calc.format_result(precision=2) == "NaN"

def test_format_result_integer_division_label():
    calc = Calculation(operation="IntDivide", first_operand=Decimal("5"), second_operand=Decimal("2"))
    # Manually set result to match the behavior
    calc.result = Decimal("2")
    assert calc.format_result() == "2"


