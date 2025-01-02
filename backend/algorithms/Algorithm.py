from abc import ABC, abstractmethod

from algorithms.AlgorithmStatistics import AlgorithmStatistics
from algorithms.TripProblem import TripProblem
from algorithms.TripState import TripState


class Algorithm(ABC):
    LOCAL_OPTIMUM_MAX_STEPS = 10
    LOCAL_OPTIMUM_MAX_ESCAPES = 15_000

    def __init__(self, problem: TripProblem, statistics: AlgorithmStatistics):
        self.problem = problem
        self.current_state = problem.initial_state
        self.statistics = statistics

        self.best_objective_value = problem.evaluate(self.current_state)
        self.best_state = problem.initial_state

        self.steps_from_last_step_update = 0

    def start(self):
        self.statistics.on_start(
            self.current_state, self.problem.evaluate(self.current_state)
        )

    @abstractmethod
    def next_state(self) -> TripState | None:
        """
        Move to the next state based on the current state
        """
        pass

    @abstractmethod
    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state
        """
        pass

    def escape_local_optimum(self) -> TripState | None:
        if self.statistics.local_optimum_escapes >= self.LOCAL_OPTIMUM_MAX_ESCAPES:
            return None

        state = self._escape_local_optimum()
        self.statistics.on_local_optimum_escape(state, self.problem.evaluate(state))
        return state

    @abstractmethod
    def _escape_local_optimum(self) -> TripState:
        pass

    def _is_stuck_in_local_optimum(self) -> bool:
        return self.steps_from_last_step_update >= self.LOCAL_OPTIMUM_MAX_STEPS
