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

    def next_state(self) -> TripState | None:
        """
        Move to the next state based on the current state
        """

        logger.debug(
            ("next_state()" f"  - Current state route: {self.current_state.route}")
        )

        next_state: TripState | None = None
        if self._is_stuck_in_local_optimum():
            next_state = self.escape_local_optimum()
        else:
            next_state = self._find_next_state()

        if next_state is not None:
            logger.debug(("next_state()" f"  - Next state route: {next_state.route}"))
            self._update_state(next_state)
        else:
            self.stop()

        return next_state

    def _update_state(self, new_state: TripState):
        logger.debug(
            (
                "_update_state()"
                f"  - Comparing with current state: {self.problem.compare_states(self.current_state, new_state)} (better when > 0)"
                f"  - Comparing with best state: {self.problem.compare_states(self.best_state, new_state)} (better when > 0)"
            )
        )

        self.statistics.on_next_state(new_state, self.problem.evaluate(new_state))

        if self.problem.compare_states(self.current_state, new_state) > 0:
            self.current_state = new_state
            self.steps_from_last_step_update = 0
        else:
            self.steps_from_last_step_update += 1
            return

        if self.problem.compare_states(self.best_state, new_state) > 0:
            self.best_objective_value = self.problem.evaluate(new_state)
            self.best_state = new_state

    def _escape_local_optimum(self) -> TripState:
        return self._random_restart()

    def _random_restart(self) -> TripState:
        return self.problem.random_valid_state()

    @abstractmethod
    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state
        """
