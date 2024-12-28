import logging
from abc import ABC, abstractmethod

from algorithms.Algorithm import Algorithm
from algorithms.AlgorithmStatistics import AlgorithmStatistics
from algorithms.TripProblem import TripProblem
from algorithms.TripState import TripState

logger = logging.getLogger(__name__)


class HillClimbing(Algorithm, ABC):
    def __init__(
        self,
        problem: TripProblem,
        algorithm_statistics: AlgorithmStatistics,
    ):
        super().__init__(problem, algorithm_statistics)

    # TODO override
    def next_state(self) -> TripState | None:
        """
        Move to the next state based on the current state
        """

        logger.debug(
            ("next_state()" f"  - Current state route: {self.current_state.route}")
        )

        # TODO stuck in local optimum
        # if stuck in local optimum: do sth
        # else:
        next_state = self._find_next_state()

        if next_state is not None:
            logger.debug(("next_state()" f"  - Next state route: {next_state.route}"))
            self._update_state(next_state)
        # else:
        # on solution

        return next_state

    @abstractmethod
    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state
        """

    def _get_available_states(self):
        states: list[TripState] = []
        for index1 in range(1, len(self.current_state.route) - 2):
            for index2 in range(index1 + 1, len(self.current_state.route) - 1):
                states.append(
                    self.problem.move_method(self.current_state, index1, index2).apply()
                )

        logger.debug(("_get_available_states()" f"  - Available states: {states}"))

        return states

    def _update_state(self, new_state: TripState):
        logger.debug(
            (
                "_update_state()"
                f"  - Comparing with current state: {self.problem.compare_states(self.current_state, new_state)} (better when > 0)"
                f"  - Comparing with best state: {self.problem.compare_states(self.best_state, new_state)} (better when > 0)"
            )
        )

        if self.problem.compare_states(self.current_state, new_state) > 0:
            self.current_state = new_state
            self.steps_from_last_step_update = 0
        else:
            self.steps_from_last_step_update += 1
            return

        if self.problem.compare_states(self.best_state, new_state) > 0:
            self.best_objective_value = self.problem.evaluate(new_state)
            self.best_state = new_state
