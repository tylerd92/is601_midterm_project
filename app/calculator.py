from decimal import Decimal
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation

Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

class Calculator:
    """
    Calculator class that performs arithmetic operations.
    """
    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Initialize the calculator with a configuration.
        @param config: Optional configuration for the calculator.
        If no configuration is provided, it will use the default configuration
        based on the project root directory.
        """
        if config is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_dir=project_root)

        self.config = config
        self.config.validate()

        os.makedirs(self.config.log_dir, exist_ok=True)
        self._setup_logging()

        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None
        self.observers: List[HistoryObserver] = []

        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []
        self._setup_directories()
        
        try:
            self.load_history()
        except Exception as e:
            logging.warning(f"Could not load existing history: {e}")
        
        logging.info("Calculator initialized with configuration")
    
    def _setup_logging(self) -> None:
        """
        Set up logging for the calculator.
        This method initializes the logging configuration based on the provided
        configuration settings. It creates the log directory if it does not exist
        and sets the logging level and format.
        @raises Exception: If there is an error setting up logging.
        @return: None
        """
        try:
            os.makedirs(self.config.log_dir, exist_ok=True)
            log_file = self.config.log_file.resolve()

            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True  # Overwrite any existing logging configuration
            )
            logging.info(f"Logging initialized at: {log_file}")
        except Exception as e:
            print(f"Error setting up logging: {e}")
            raise


    def _setup_directories(self) -> None:
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

    def add_observer(self, observer: HistoryObserver) -> None:
        """
        Add an observer to the calculator.
        @param observer: An instance of HistoryObserver that will be notified when a Calculation is performed.
        """
        self.observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")

    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        Remove an observer from the calculator.
        @param observer: An instance of HistoryObserver to be removed.
        @return: None
        """
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        """
        Notify all observers about a new calculation.
        This method iterates through all registered observers and calls their
        update method with the new Calculation object.
        @param calculation: The Calculation object that has been performed.
        @return: None
        """
        for observer in self.observers:
            observer.update(calculation)

    def set_operation(self, operation: Operation) -> None:
        """
        Set the current operation strategy.
        @param operation: An instance of Operation that defines the arithmetic operation to be performed.
        @return: None
        """
        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")

    def perform_operation(
        self,
        a: Union[str, Number],
        b: Union[str, Number]
    ) -> CalculationResult:
        """
        Perform a calculation using the current operation strategy.
        @param a: The first operand, can be a string or a number.
        @param b: The second operand, can be a string or a number.
        @return: The result of the operation.
        @raises OperationError: If no operation is set or if the operation fails.
        @raises ValidationError: If the input validation fails.
        @raises Exception: If there is an unexpected error during the operation.
        """
        if not self.operation_strategy:
            raise OperationError("No operation set")
        
        try:
            validated_a = InputValidator.validate_number(a, self.config)
            validated_b = InputValidator.validate_number(b, self.config)

            result = self.operation_strategy.execute(validated_a, validated_b)
            calculation = Calculation(
                operation=str(self.operation_strategy),
                first_operand=validated_a,
                second_operand=validated_b
            )

            self.undo_stack.append(CalculatorMemento(self.history.copy()))
            self.redo_stack.clear()
            self.history.append(calculation)

            if len(self.history) > self.config.max_history_size:
                self.history.pop(0) # pragma: no cover
            
            self.notify_observers(calculation)
            return result
        except ValidationError as e:
            logging.error(f"Validation error: {str(e)}")
            raise
        except Exception as e: # pragma: no cover
            logging.error(f"Validation error: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")
        
    def save_history(self) -> None:
        """
        Save the calculation history to a file.
        This method creates the history directory if it does not exist,
        and saves the history to a CSV file.
        @raises OperationError: If there is an error saving the history.
        @return: None
        """
        try:
            self.config.history_dir.mkdir(parents=True, exist_ok=True)
            history_data = []
            for calc in self.history:
                history_data.append({
                    'operation': str(calc.operation),
                    'first_operand': str(calc.first_operand),
                    'second_operand': str(calc.second_operand),
                    'result': str(calc.result),
                    'timestamp': calc.timestamp.isoformat()
                })
            
            if history_data:
                df = pd.DataFrame(history_data)
                df.to_csv(self.config.history_file, index=False)
                logging.info(f"History saved successfully to {self.config.history_file}")
            else: 
                pd.DataFrame(columns=['operation', 'first_operand', 'second_operand', 'result', 'timestamp']
                             ).to_csv(self.config.history_file, index=False)
                logging.info("Empty history saved")
        except Exception as e:
            logging.error(f"Failed to save history: {e}")
            raise OperationError(f"Failed to save history: {e}")
        
    def load_history(self) -> None:
        """
        Load the calculation history from a CSV file.
        This method reads the history from the configured history file
        and populates the history list with Calculation objects.
        @raises OperationError: If there is an error loading the history.
        @return: None
        """
        try:
            if self.config.history_file.exists():
                df = pd.read_csv(self.config.history_file)
                if not df.empty:
                    self.history = [
                        Calculation.from_dict({
                            'operation': row['operation'],
                            'first_operand': row['first_operand'],
                            'second_operand': row['second_operand'],
                            'result': row['result'],
                            'timestamp': row['timestamp']
                        })
                        for _, row in df.iterrows()
                    ]
                    logging.info(f"Loaded {len(self.history)} calculations from history")
                else:
                    logging.info("Loaded empty history file")
            else:
                logging.info("No history file found - starting with empty history")
        except Exception as e: # pragma: no cover
            logging.error(f"Failed to load history: {e}")
            raise OperationError(f"Failed to load history: {e}")
        
    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Get the calculation history as a Pandas DataFrame.
        @return: A DataFrame containing the history of calculations.
        This method is useful for analyzing or displaying the history in a tabular format.
        @raises OperationError: If there is an error converting the history to a DataFrame.
        @raises ValidationError: If the history is empty or invalid.
        @return: A Pandas DataFrame containing the history of calculations.
        """
        history_data = []
        for calc in self.history:
            history_data.append({
                'operation': str(calc.operation),
                'first_operand': str(calc.first_operand),
                'second_operand': str(calc.second_operand),
                'result': str(calc.result),
                'timestamp': calc.timestamp
            })
        return pd.DataFrame(history_data)
    
    def show_history(self) -> List[str]:
        """
        Show the calculation history as a list of strings.
        @return: A list of strings representing the history of calculations.
        This method formats each calculation in the history as a string
        in the format "operation(first_operand, second_operand) = result".
        """
        return [
            f"{calc.operation}({calc.first_operand}, {calc.second_operand}) = {calc.result}"
            for calc in self.history
        ]
    
    def clear_history(self) -> None:
        """
        Clear the calculation history.
        This method clears the history list, undo stack, and redo stack.
        @return: None
        """
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("History cleared")

    def undo(self) -> bool:
        """
        Undo the last calculation.
        This method restores the previous state of the calculator from the undo stack.
        @return: True if the undo was successful, False otherwise.
        """
        if not self.undo_stack:
            return False
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True
    
    def redo(self) -> bool:
        """
        Redo the last undone calculation.
        This method restores the next state of the calculator from the redo stack.
        @return: True if the redo was successful, False otherwise.
        """
        if not self.redo_stack:
            return False
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True