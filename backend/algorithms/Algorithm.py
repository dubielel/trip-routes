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

    def time_elapsed(self) -> float:
        return self.statistics.time_elapsed()

    def stop(self):
        self.statistics.on_solution(self.best_state, self.best_objective_value)

    def escape_local_optimum(self) -> TripState | None:
        if self.statistics.local_optimum_escapes >= self.LOCAL_OPTIMUM_MAX_ESCAPES:
            return None

        state = self._escape_local_optimum()
        self.statistics.on_local_optimum_escape(state, self.problem.evaluate(state))
        return state

    def _get_available_states(self):
        states: list[TripState] = []
        for index1 in range(1, len(self.current_state.route) - 2):
            for index2 in range(index1 + 1, len(self.current_state.route) - 1):
                neighbour = self.problem.move_method(
                    self.current_state, index1, index2
                ).apply()
                self.statistics.on_next_neighbour(
                    neighbour, self.problem.evaluate(neighbour)
                )
                states.append(neighbour)

        return states

    def _is_stuck_in_local_optimum(self) -> bool:
        return self.steps_from_last_step_update >= self.LOCAL_OPTIMUM_MAX_STEPS

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

    @abstractmethod
    def _update_state(self, new_state: TripState):
        pass

    @abstractmethod
    def _escape_local_optimum(self) -> TripState:
        pass
