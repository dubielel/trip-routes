import logging

from algorithms.TripState import TripState
from algorithms.hill_climbing.HillClimbing import HillClimbing

logger = logging.getLogger(__name__)


class FirstChoiceHillClimbing(HillClimbing):
    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state.

        The first improving neighbour is chosen.
        """

        logger.debug("_find_next_state()")

        # Most basic hill climbing - first improving neighbour is chosen
        # Probably can make this method abstract and implement more advanced hill climbing algorithms
        for neighbour in self._get_available_states():
            if self.problem.compare_states(self.current_state, neighbour) > 0:
                logger.debug(
                    (
                        "_find_next_state()"
                        f"  - Found first improving neighbour route: {neighbour.route}"
                    )
                )
                return neighbour

        return self.current_state
