import pytest
from unittest.mock import Mock, patch
from app.calculation import Calculation
from app.logger import LoggingObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "addition"
calculation_mock.first_operand = 4
calculation_mock.second_operand = 3
calculation_mock.result = 7

@patch('logging.info')
def test_logging_observer_logs_calculation(logging_info_mock):
    observer = LoggingObserver()
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with(
        "Calculation performed: addition (4, 3) = 7"
    )

def test_logging_observer_no_calculation():
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)