from abc import ABC, abstractmethod

from algorithms.TripState import TripState


class Move(ABC):
    @abstractmethod
    def apply(self) -> TripState:
        """
        Apply the move to the current state and return the new state
        """
        pass

    @abstractmethod
    def _is_valid(self) -> bool:
        """
        Check if the move is valid
        """
        pass
