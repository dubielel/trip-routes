import logging

from random import choice, random
from math import exp

from algorithms.Algorithm import Algorithm
from algorithms.AlgorithmStatistics import AlgorithmStatistics
from algorithms.TripProblem import TripProblem
from algorithms.TripState import TripState


logger = logging.getLogger(__name__)


class SimulatedAnnealing(Algorithm):
    # TODO work on hyperparameters
    INITIAL_TEMPERATURE = 1_000_000
    COOLING_SCHEDULE = 0.999
    REHEAT_RATIO = 0.05
    MIN_TEMPERATURE = 60

    LOCAL_OPTIMUM_MAX_ESCAPES = 1_000

    def __init__(
        self,
        problem: TripProblem,
        algorithm_statistics: AlgorithmStatistics,
    ):
        self.temperature = self.INITIAL_TEMPERATURE

        super().__init__(problem, algorithm_statistics)

    def next_state(self) -> TripState | None:
        """
        Move to the next state based on the current state
        """

        next_state: TripState | None = None
        if self._is_stuck_in_local_optimum():
            next_state = self.escape_local_optimum()
        else:
            next_state = self._find_next_state()

        if next_state is not None:
            self._update_state(next_state)
        else:
            self.stop()

        self._update_temperature()

        return next_state

    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state
        """
        return choice(self._get_available_states())

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

    def _update_state(self, new_state: TripState):
        self.statistics.on_next_state(new_state, self.problem.evaluate(new_state))
        if random() <= self._calculate_update_probability(new_state):
            if self.problem.compare_states(self.current_state, new_state) < 0:
                self.statistics.on_worse_next_state()

            self.current_state = new_state
            self.steps_from_last_step_update = 0
        else:
            self.steps_from_last_step_update += 1
            return

        if self.problem.compare_states(self.best_state, new_state) > 0:
            self.best_objective_value = self.problem.evaluate(new_state)
            self.best_state = new_state

            self.statistics.best_states_list.append(
                (
                    new_state.route,
                    self.best_objective_value,
                    self.statistics.time_elapsed(),
                )
            )

    def _calculate_update_probability(self, new_state: TripState) -> float:
        """
        Calculate the probability of updating the current state to the new state
        using the Metropolis criterion:

        ΔE - the difference between the new state and the current state objective values

        When ΔE > 0, the new state is better than the current state
        and it is always accepted, so the probability is 1.0

        Otherwise, the probability is calculated as:
        exp(-ΔE / T), where T is the temperature
        """

        improvement_against_current = self.problem.compare_states(
            self.current_state, new_state
        )

        if improvement_against_current > 0:
            return 1.0

        # In this case, ΔE is `improvement_against_current` which is negative,
        # so the formula becomes exp(ΔE / T)
        return exp(improvement_against_current / self.temperature)

    def _update_temperature(self) -> None:
        """
        Update the temperature based on the cooling schedule
        """

        new_temperature = self.temperature * self.COOLING_SCHEDULE

        if new_temperature <= self.MIN_TEMPERATURE:
            self.temperature = self.MIN_TEMPERATURE
            return

        self.temperature = new_temperature

    def _escape_local_optimum(self) -> TripState:
        return self._random_restart_and_reheat()

    def _random_restart_and_reheat(self) -> TripState:
        reheat_temperature = self.INITIAL_TEMPERATURE * self.REHEAT_RATIO
        if self.temperature < reheat_temperature:
            self.temperature = reheat_temperature
        return self.problem.random_valid_state()
