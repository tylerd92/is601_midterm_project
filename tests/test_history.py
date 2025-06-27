import pytest
from unittest.mock import Mock, patch
from app.calculation import Calculation
from app.logger import AutoSaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "addition"
calculation_mock.first_operand = 4
calculation_mock.second_operand = 3
calculation_mock.result = 7

def test_autosave_observer_triggers_save():
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_called_once()

@patch('logging.info')
def test_autosave_observer_logs_autosave(logging_info_mock):
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with("History auto-saved")

def test_autosave_observer_does_not_trigger_save_when_disabled():
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    with pytest.raises(AttributeError):
        observer.update(None)

def test_autosave_observer_init_missing_config():
    calculator_mock = Mock()
    del calculator_mock.config
    calculator_mock.save_history = Mock()
    with pytest.raises(TypeError):
        AutoSaveObserver(calculator_mock)
