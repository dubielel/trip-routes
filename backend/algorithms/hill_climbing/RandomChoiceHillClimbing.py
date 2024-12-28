import logging
from random import choice as random_chcoice

from algorithms.TripState import TripState
from algorithms.hill_climbing.HillClimbing import HillClimbing

logger = logging.getLogger(__name__)


class RandomChoiceHillClimbing(HillClimbing):
    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state.

        A random improving neighbour is chosen.
        """

        logger.debug("_find_next_state()")

        neighbours = self._get_available_states()

        # TODO what about plateau? Don't we want to move around the plateau hoping to find a better solution? Probably we would want to

        # There is no better neighbour
        if all(
            [
                self.problem.compare_states(self.current_state, neighbour) <= 0
                for neighbour in neighbours
            ]
        ):
            return None

        random_neighbour = random_chcoice(neighbours)
        while self.problem.compare_states(self.current_state, random_neighbour) <= 0:
            random_neighbour = random_chcoice(neighbours)

        return random_neighbour
