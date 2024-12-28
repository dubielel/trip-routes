from copy import deepcopy
import logging

from algorithms.moves.Move import Move
from algorithms.TripState import TripState

logger = logging.getLogger(__name__)


class SwapTwoPoints(Move):
    def __init__(self, state: TripState, index1: int, index2: int):
        self.state = state
        self.index1, self.index2 = index1, index2

        if not self._is_valid():
            raise ValueError(
                "Invalid indices - cannot swap the first or the last element"
            )

    def apply(self) -> TripState:
        new_route = deepcopy(self.state.route)

        logger.debug(
            f"Swapping {new_route[self.index1]} at index {self.index1} and {new_route[self.index2]} at index {self.index2} in {new_route}"
        )

        new_route[self.index1], new_route[self.index2] = (
            new_route[self.index2],
            new_route[self.index1],
        )

        return TripState(self.state.all_places, new_route)

    def _is_valid(self) -> bool:
        """
        Check if the indices are valid
        (none of them can be the first or the last element of the route)
        """

        return all(
            [
                0 < self.index1 < len(self.state.route) - 1,
                0 < self.index2 < len(self.state.route) - 1,
            ]
        )
