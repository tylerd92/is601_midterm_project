from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation

@dataclass
class CalculatorMemento:
    """
    Memento class that stores the state of the calculator.
    """
    history: List[Calculation]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    """
    Convert the memento to a dictionary representation.
    @return: A dictionary containing the history and timestamp.
    This method is useful for serialization or saving the state to a file.
    """
    def to_dict(self) -> Dict[str, Any]:
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }
    
    """
    Create a CalculatorMemento instance from a dictionary representation.
    @param data: A dictionary containing the history and timestamp.
    @return: A CalculatorMemento instance.
    """
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculatorMemento':
        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )