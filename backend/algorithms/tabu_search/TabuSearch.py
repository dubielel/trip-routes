import logging

from algorithms.Algorithm import Algorithm
from algorithms.AlgorithmStatistics import AlgorithmStatistics
from algorithms.TripProblem import TripProblem
from algorithms.TripState import TripState


logger = logging.getLogger(__name__)


class TabuSearch(Algorithm):
    MAX_TABU_LIST_SIZE = (
        500  # TODO find a good value for this or implement a dynamic tabu list size
    )
    tabu_list: list[TripState]

    def __init__(
        self,
        problem: TripProblem,
        algorithm_statistics: AlgorithmStatistics,
    ):
        self.tabu_list = []

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

            self.tabu_list.append(next_state)
            if len(self.tabu_list) > self.MAX_TABU_LIST_SIZE:
                self.tabu_list.pop(0)
        else:
            self.statistics.on_solution(self.best_state, self.best_objective_value)

        return next_state

    def _find_next_state(self) -> TripState | None:
        """
        Find the next state based on the current state
        """

        best_candidate: TripState | None = None

        for neighbour in self._get_available_states():
            if neighbour in self.tabu_list:
                continue

            if best_candidate is None:
                best_candidate = neighbour
                continue

            if self.problem.compare_states(best_candidate, neighbour) > 0:
                best_candidate = neighbour

        return best_candidate or self.current_state

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

        self.statistics.on_next_state(new_state, self.problem.evaluate(new_state))

        if new_state == self.current_state:
            self.steps_from_last_step_update += 1
            return

        if self.problem.compare_states(self.current_state, new_state) < 0:
            self.statistics.on_worse_next_state()

        self.current_state = new_state
        self.steps_from_last_step_update = 0

        if self.problem.compare_states(self.best_state, new_state) > 0:
            self.best_objective_value = self.problem.evaluate(new_state)
            self.best_state = new_state

    def _escape_local_optimum(self) -> TripState:
        return self._random_restart()

    def _random_restart(self) -> TripState:
        return self.problem.random_valid_state()
