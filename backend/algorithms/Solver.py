import logging

from algorithms.Algorithm import Algorithm
from algorithms.TripProblem import TripProblem
from algorithms.TripState import TripState

logger = logging.getLogger(__name__)


class Solver:
    MAX_TIME = 60

    def __init__(self, problem: TripProblem, algorithm: Algorithm):
        self.problem = problem
        self.algorithm = algorithm

    def solve(self) -> TripState:
        logger.debug("Solving starts")

        self.algorithm.start()
        solution_state = self.problem.initial_state

        # TODO only timeout or should the solving end when algorithm is stuck in optimum?
        while not self._is_timeout():
            logger.debug(f"Time elapsed: {self.algorithm.time_elapsed()}")
            next_state = self.algorithm.next_state()

            if next_state is None:
                solution_state = self.algorithm.best_state
                logger.debug(
                    f"No next state - algorithm finishes with best state: {solution_state.route}"
                )
                break

            logger.debug(f"Solver Next state: {next_state.route}")
            solution_state = next_state

        else:
            logger.debug("Timeout - algorithm interrupted")
            self.algorithm.stop()
            solution_state = self.algorithm.best_state

        logger.debug(f"Solving ends - solution state: {solution_state.route}")
        return solution_state

    def _is_timeout(self) -> bool:
        return self.algorithm.time_elapsed() > self.MAX_TIME
