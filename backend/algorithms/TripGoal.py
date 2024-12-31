from enum import Enum
import numpy as np
import numpy.typing as npt
import logging

from algorithms.TripState import TripState

logger = logging.getLogger(__name__)


class GoalType(Enum):
    MINIMIZE = -1
    MAXIMIZE = 1


class TripGoal:
    def __init__(self, time_matrix: npt.NDArray[np.float64], max_seconds_per_day: int):
        self.time_matrix = time_matrix
        self.max_seconds_per_day = max_seconds_per_day

    @staticmethod
    def goal_type() -> GoalType:
        """
        Goal type for this objective is to minimize the time
        """
        return GoalType.MINIMIZE

    def evaluate(self, state: TripState) -> float:
        """
        Evaluate the state for the objective
        """

        logger.debug(
            (
                "Evaluating objective for:"
                f"  - State: {state}"
                f"  - Route: {state.route}"
            )
        )

        if not self.is_state_valid(state):
            return float("inf")

        # Calculate total trip time
        trip_time = 0.0
        for start_place_index, end_place_index in zip(
            state.route[:-1], state.route[1:]
        ):
            trip_time += self.time_matrix[start_place_index][end_place_index]

        logger.debug(
            (
                "Evaluating objective for:"
                f"  - State: {state}"
                f"  - Route: {state.route}"
                f"  - Trip time: {trip_time}"
            )
        )

        return trip_time

    def is_state_valid(self, state: TripState) -> bool:
        """
        Check if time needed for each day does not exceed the day limit
        """

        current_accommodation_index = 0
        while current_accommodation_index < len(state.route) - 1:
            next_accommodation_index = state.route.index(
                0, current_accommodation_index + 1
            )

            day_trip = state.route[
                current_accommodation_index : next_accommodation_index + 1
            ]
            day_time = 0.0

            for start_place_index, end_place_index in zip(day_trip[:-1], day_trip[1:]):
                day_time += self.time_matrix[start_place_index][end_place_index]

            logger.debug(
                (
                    "Evaluating objective - daily:"
                    f"  - Day trip: {day_trip}"
                    f"  - Day time: {day_time} -> exceeds maximal time per day?: {day_time > self.max_seconds_per_day}"
                )
            )

            if day_time > self.max_seconds_per_day:
                logger.warning(
                    (
                        "Evaluating objective - exceeded maximal day time:"
                        f"  - Route: {state.route}"
                        f"  - Day trip: {day_trip}"
                    )
                )
                return False

            current_accommodation_index = next_accommodation_index

        return True
