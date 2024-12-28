import logging

from algorithms.TripState import TripState
from algorithms.hill_climbing.HillClimbing import HillClimbing

logger = logging.getLogger(__name__)


class BestChoiceHillClimbing(HillClimbing):
    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state.

        After comparing all neighbours to the current state, the best neighbour is chosen.
        """

        logger.debug("_find_next_state()")

        neighbours = self._get_available_states()
        improvements = [
            self.problem.compare_states(self.current_state, neighbour)
            for neighbour in neighbours
        ]

        best_neighbour = neighbours[improvements.index(max(improvements))]
        if self.problem.compare_states(self.current_state, best_neighbour) > 0:
            logger.debug(
                (
                    "_find_next_state()"
                    f"- Found best neighbour route: {best_neighbour.route}"
                )
            )

            return best_neighbour

        return None
