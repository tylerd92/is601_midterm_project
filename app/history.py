from abc import ABC, abstractmethod
from app.calculation import Calculation

class HistoryObserver(ABC):
    """
    An abstract observer class that listens for updates to a Calculation.

    This class should be implemented by any observer that wants to receive
    updates when a Calculation is created or modified.
    @param Calculation: The Calculation object that is being observed.
    """
    @abstractmethod
    def update(self, calulation: Calculation) -> None:
        pass # pragma: no cover

