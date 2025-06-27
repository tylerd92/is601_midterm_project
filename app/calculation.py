from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict
from app.exceptions import OperationError

@dataclass
class Calculation:
    operation: str
    first_operand: Decimal
    second_operand: Decimal

    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.result = self.calculate()

    def calculate(self) -> Decimal:
        """
        Perform the calculation based on the operation and operands.
        @return: The result of the calculation.
        @raises OperationError: If the operation is invalid or if an error occurs during calculation.
        """
        operations = {
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": lambda x, y: x / y if y != 0 else self._raise_div_zero(),
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._raise_neg_power(),
            "Root": lambda x, y: (
                Decimal(pow(float(x), 1 / float(y))) 
                if x >= 0 and y != 0 
                else self._raise_invalid_root(x, y)
            ),
            "Modulus": lambda x, y: x % y if y != 0 else self._raise_div_zero(),
            "IntegerDivison": lambda x, y: x // y if y != 0 else self._raise_div_zero(),
            "Percent": lambda x, y: (x / y * 100) if y != 0 else self._raise_div_zero(),
            "AbsoluteDifference": lambda x, y: abs(x - y)
        }

        op = operations.get(self.operation)
        if not op: 
            raise OperationError(f"Unknown operation: {self.operation}")
        
        try:
            return op(self.first_operand, self.second_operand)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            raise OperationError(f"Calculation failed: {str(e)}")
        
    @staticmethod
    def _raise_div_zero():
        """
        Raise an error for division by zero.
        """
        raise OperationError("Division by zero is not allowed")
    
    @staticmethod
    def _raise_neg_power():
        """
        Raise an error for negative exponentiation.
        """
        raise OperationError("Negative exponents are not supported")
    
    @staticmethod
    def _raise_invalid_root(x: Decimal, y: Decimal):
        """
        Raise an error for invalid root operations.
        """
        if y == 0:
            raise OperationError("Zero root is undefined")
        if x < 0:
            raise OperationError("Cannot calculate root of negative number")
        raise OperationError("Invalid root operation")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'operation': self.operation,
            'first_operand': str(self.first_operand),
            'second_operand': str(self.second_operand),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        """
        Create a Calculation instance from a dictionary.
        @param data: Dictionary containing calculation data.
        @return: A Calculation instance.
        @raises OperationError: If the data is invalid or missing required fields.
        """
        try:
            calc = Calculation(
                operation=data['operation'],
                first_operand=Decimal(data['first_operand']),
                second_operand=Decimal(data['second_operand'])
            )

            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])
            saved_result = Decimal(data['result'])

            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.result}"
                )
            
            return calc
        except (KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")
        
    def __str__(self) -> str:
        return f"{self.operation}({self.first_operand}, {self.second_operand}) = {self.result}"
    
    def __repr__(self) -> str:
        return (
            f"Calculation(operation='{self.operation}', "
            f"first_operand={self.first_operand}, "
            f"second_operand={self.second_operand}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.first_operand == other.first_operand and
            self.second_operand == other.second_operand and
            self.result == other.result
        )
    
    def format_result(self, precision: int = 10) -> str:
        """
        Format the result of the calculation.
        @param precision: Number of decimal places to round the result.
        @return: A string representation of the result rounded to the specified precision.
        @raises InvalidOperation: If the result cannot be formatted.
        """
        try:
            if self.operation == "IntegerDivision":
                return str(int(self.result))
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation:
            return str(self.result)