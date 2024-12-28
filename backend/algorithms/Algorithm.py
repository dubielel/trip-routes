from abc import ABC, abstractmethod

from algorithms.AlgorithmStatistics import AlgorithmStatistics
from algorithms.TripProblem import TripProblem
from algorithms.TripState import TripState


class Algorithm(ABC):
    best_objective_value: float
    best_state: TripState

    steps_from_last_step_update: int

    def __init__(self, problem: TripProblem, algorithm_statistics: AlgorithmStatistics):
        self.problem = problem
        self.current_state = problem.initial_state
        self.algorithm_statistics = algorithm_statistics

        self.best_objective_value = problem.evaluate(self.current_state)
        self.best_state = problem.initial_state
        self.steps_from_last_step_update = 0

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
