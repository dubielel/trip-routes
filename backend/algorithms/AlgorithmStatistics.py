from collections import Counter
from typing import Any, Counter as CounterType
from time import time
from datetime import datetime

from algorithms.TripState import TripState


class AlgorithmStatistics:
    def __init__(self, algorithm_name: str, move_method_name: str):
        self.algorithm_name = algorithm_name
        self.move_method_name = move_method_name

        self.start_time: float | None = None
        self.end_time: float | None = None
        self.total_time: float = 0.0

        self.initial_state: TripState | None = None
        self.initial_state_value: float | None = None

        self.restart_states: CounterType[TripState] = Counter()

        self.solution_state: TripState | None = None
        self.solution_state_value: float | None = None

        self.explored_states: CounterType[TripState] = Counter()
        """
        States that were produced as neighbours of the current state
        """
        self.explored_states_count: int = 0
        self.distinct_explored_states_count: int = 0

        self.visited_states: CounterType[TripState] = Counter()
        """
        States that were visited during the algorithm execution (current states)
        """
        self.visited_states_count: int = 0
        self.distinct_visited_states_count: int = 0

        self.local_optimum_escapes: int = 0

        self.worsening_moves: int = 0

        self.states: dict[str, float] = {}

        # route, value (None if inf), time, probability
        self.visited_states_list: list[
            tuple[tuple[int, ...], float | None, float, float]
        ] = []

        # route, value (None if inf), time
        self.best_states_list: list[tuple[tuple[int, ...], float | None, float]] = []

    def on_start(self, initial_state: TripState, value: float):
        self.initial_state = initial_state
        self.initial_state_value = value
        self._start_timer()

    def on_next_state(self, state: TripState, value: float):
        self.visited_states[state] += 1
        self.states[str(state.route)] = value

    def on_worse_next_state(self):
        self.worsening_moves += 1

    def on_next_neighbour(self, state: TripState, value: float):
        self.explored_states[state] += 1
        self.states[str(state.route)] = value

    def on_local_optimum_escape(self, next_state: TripState, value: float):
        self.restart_states[next_state] += 1
        self.local_optimum_escapes += 1
        self.states[str(next_state.route)] = value

    def on_solution(self, solution_state: TripState, value: float):
        self._stop_timer()

        self.solution_state = solution_state
        self.solution_state_value = value

        self.explored_states_count = sum(self.explored_states.values())
        self.distinct_explored_states_count = len(self.explored_states)

        self.visited_states_count = sum(self.visited_states.values())
        self.distinct_visited_states_count = len(self.visited_states)

    def time_elapsed(self) -> float:
        return time() - self.start_time

    def _start_timer(self) -> None:
        self.start_time = time()
        self.total_time = 0.0

    def _stop_timer(self) -> None:
        self.end_time = time()
        self.total_time = self.end_time - self.start_time

    def to_dict(self) -> dict[str, Any]:
        return {
            "algorithmName": self.algorithm_name,
            "moveMethodName": self.move_method_name,
            "startTimestamp": self.start_time,
            "startTime": (
                datetime.fromtimestamp(self.start_time).isoformat()
                if self.start_time
                else None
            ),
            "endTimestamp": self.end_time,
            "endTime": (
                datetime.fromtimestamp(self.end_time).isoformat()
                if self.end_time
                else None
            ),
            "totalTime": self.total_time,
            "initialState": str(self.initial_state.route)
            if self.initial_state
            else None,
            "initialStateValue": self.initial_state_value,
            "solutionState": str(self.solution_state.route)
            if self.solution_state
            else None,
            "solutionStateValue": self.solution_state_value,
            "exploredStatesCount": self.explored_states_count,
            "distinctExploredStatesCount": self.distinct_explored_states_count,
            "visitedStatesCount": self.visited_states_count,
            "distinctVisitedStatesCount": self.distinct_visited_states_count,
            "localOptimumEscapes": self.local_optimum_escapes,
            "worseningMoves": self.worsening_moves,
            "restartStates": {
                str(state.route): count for state, count in self.restart_states.items()
            },
            "exploredStates": {
                str(state.route): count for state, count in self.explored_states.items()
            },
            "visitedStates": {
                str(state.route): count for state, count in self.visited_states.items()
            },
            "states": {
                route: (value if value != float("inf") else None)
                for route, value in self.states.items()
            },
        }
