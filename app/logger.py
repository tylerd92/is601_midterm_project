import logging
from typing import Any
from app.calculation import Calculation
from app.history import HistoryObserver

class LoggingObserver(HistoryObserver):
    """
    Observer that logs calculation events.
    This observer logs the details of each calculation performed.
    It is useful for debugging and tracking the history of calculations.
    @param Calculation: The Calculation object that is being observed.
    @raises AttributeError: If the Calculation is None.
    """
    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.first_operand}, {calculation.second_operand}) = "
            f"{calculation.result}"
        )

class AutoSaveObserver(HistoryObserver):
    """
    Observer that automatically saves calculation history.
    This observer checks the calculator's configuration and saves the history
    if the auto-save feature is enabled.
    @param calculator: The calculator instance that is being observed.
    @raises TypeError: If the calculator does not have the required attributes.
    """
    def __init__(self, calculator: Any) -> None:
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator
    """
    Update method that saves the calculation history.
    This method is called whenever a Calculation is updated.
    It checks if the auto-save feature is enabled in the calculator's configuration and saves the history if it is.
    @param calculation: The Calculation object that is being observed.
    @raises AttributeError: If the Calculation is None.
    """
    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")