"""
This module defines custom exceptions for the calculator application.
These exceptions are used to handle various error scenarios such as validation errors, operation errors, and configuration errors. Each exception inherits from a base exception class.
"""
class CalculatorError(Exception):
    pass

class ValidationError(CalculatorError):
    pass

class OperationError(CalculatorError):
    pass

class ConfigurationError(CalculatorError):
    pass