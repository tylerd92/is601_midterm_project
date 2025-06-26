from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, List
from app.exceptions import ValidationError

class Operation(ABC):
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__
    
class Addition(Operation):
    """
    @param a: First operand.
    @param b: Second operand.
    @return: The sum of a and b.
    This method validates the operands and returns their sum.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a + b
    
class Subtraction(Operation):
    """
    @param a: First operand.
    @param b: Second operand.
    @return: The difference of a and b.
    This method validates the operands and returns their difference.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a - b
    
class Multiplication(Operation):
    """
    @param a: First operand.
    @param b: Second operand.
    @return: The product of a and b.
    This method validates the operands and returns their product.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a * b

class Division(Operation):
    """
    @param a: First operand.
    @param b: Second operand.
    @return: The quotient of a and b.
    This method validates the operands and returns their quotient.
    It raises a ValidationError if b is zero to prevent division by zero.
    """
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")
        
    """
    @param a: First operand.
    @param b: Second operand.
    @return: The quotient of a and b.
    This method executes the division operation after validating the operands.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a / b

class Power(Operation):
    """
    @param a: Base operand.
    @param b: Exponent operand.
    This method validates the operands and returns a raised to the power of b.
    It raises a ValidationError if b is negative, as negative exponents are not supported.
    """
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")
    
    """
    @param a: Base operand.
    @param b: Exponent operand.
    @return: The result of a raised to the power of b.
    This method executes the power operation after validating the operands.
    It uses float conversion to handle large numbers and avoid overflow.
    It returns a Decimal result.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))
    
class Root(Operation):
    """
    This method validates the operands
    It raises a ValidationError if a is negative or b is zero, as these cases are undefined.
    """
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")
        
    """
    @param a: The number to calculate the root of.
    @param b: The degree of the root.
    @return: The b-th root of a.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))
        
class Modulus(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed")

    """
    @param a: First operand.
    @param b: Second operand.
    @return: The modulus of a by b.
    This method validates the operands and returns the modulus of a by b.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a % b
    
class IntDivide(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divide by zero is not allowed")
    
    """
    @param a: First operand.
    @param b: Second operand.
    @return: The result of integer division of a by b.
    This method validates the operands and performs integer division.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a // b
        
class Percent(Operation):
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divide by zero is not allowed")
    
    """
    @param a: First operand.
    @param b: Second operand.
    @return: The percentage of a with respect to b.
    This method validates the operands and returns the percentage of a with respect to b.
    It raises a ValidationError if b is zero to prevent division by zero.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return (a / b) * 100


class AbsoluteDifference(Operation):
    
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)

    """
    @param a: First operand.
    @param b: Second operand.
    @return: The absolute difference between a and b.
    This method validates the operands and returns the absolute difference.
    """
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return abs(a - b)


class OperationFactory:
    """
    Factory class to create operation instances.
    It supports registering new operations dynamically.
    """
    _operations: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'int_divide': IntDivide,
        'percent': Percent,
        'abs_diff': AbsoluteDifference
    }

    """
    @param name: The name of the operation to register.
    @param operation_class: The class of the operation to register.
    This method allows dynamic registration of new operations.
    It raises a TypeError if the provided class does not inherit from Operation.
    """
    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    """
    @param operation_type: The type of the operation to create.
    @return: An instance of the requested operation.
    This method creates an instance of the requested operation type.
    It raises a ValueError if the operation type is unknown.
    """
    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()
    
    """
    @param cls: The class itself.
    @return: A list of all registered operation names.
    This method returns a list of all registered operation names.
    """
    @classmethod
    def get_operations(cls) -> List[str]:
        return list(cls._operations.keys())
    
