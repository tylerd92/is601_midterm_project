from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

@dataclass
class InputValidator:
    """
    This class provides methods to validate user input for the calculator application.
    It includes methods to validate numbers, ensuring they conform to the specified configuration.
    """
    @staticmethod
    def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
        """
        Validates the input number against the specified configuration.
        @param value: The input value to validate, can be int, float, str, or Decimal.
        @param config: The configuration object containing validation parameters.
        @return: A Decimal representation of the validated number.
        @raises ValidationError: If the input is not a valid number or exceeds the maximum allowed value.
        """
        try:
            if isinstance(value, str):
                value = value.strip()
            number = Decimal(str(value))
            if abs(number) > config.max_input_value:
                raise ValidationError(f"Value exceeds maximum allowed: {config.max_input_value}")
            return number.normalize()
        except InvalidOperation as e:
            raise ValidationError(f"Invalid number format: {value}") from e