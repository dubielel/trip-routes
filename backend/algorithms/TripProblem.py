import logging

from datetime import datetime
from copy import deepcopy
from geojson_pydantic import FeatureCollection, Feature, Point
import numpy as np

from algorithms.TripGoal import TripGoal
from algorithms.TripState import TripState
from algorithms.moves.Move import Move
from models.api.CalculateTripRequestBody import CalculateTripRequestBody
from pgrouting.PgRouting import PgRouting

logger = logging.getLogger(__name__)


class TripProblem:
    all_places: FeatureCollection[Feature[Point, dict]]
    """
    All places to visit including accommodation at the beginning of the list
    """

    def __init__(self, trip_params: CalculateTripRequestBody, move_method: Move):
        self.trip_params = trip_params

        self.all_places = deepcopy(trip_params.placesToVisit)
        self.all_places.features.insert(0, trip_params.accommodation)

        self.number_of_nights = (
            datetime.fromtimestamp(trip_params.lastDayTimestamp // 1000)
            - datetime.fromtimestamp(trip_params.firstDayTimestamp // 1000)
        ).days

        self.max_seconds_per_day = (
            datetime.fromtimestamp(trip_params.dayEndTimestamp // 1000)
            - datetime.fromtimestamp(trip_params.dayStartTimestamp // 1000)
        ).seconds

        self.time_matrix = self._calculate_time_matrix()

        self.goal_evaluator = TripGoal(self.time_matrix, self.max_seconds_per_day)
        self.move_method = move_method

        self.initial_state = self._initial_state()

        logger.info(
            f"Initialized TripProblem with {self.move_method.__name__} move method"
        )
        logger.debug(
            (
                "TripProblem:"
                f"  - All places: {self.all_places}"
                f"  - Number of nights: {self.number_of_nights}"
                f"  - Max seconds per day: {self.max_seconds_per_day}"
                f"  - Time matrix: {self.time_matrix}"
                f"  - Move method: {self.move_method.__name__}"
            )
        )

    def compare_states(self, current_state: TripState, next_state: TripState):
        current_state_time = self.evaluate(current_state)
        next_state_time = self.evaluate(next_state)

        time_diff = next_state_time - current_state_time

        improvement = time_diff * self.goal_evaluator.goal_type().value

        logger.debug(
            (
                "Comparing states:"
                f"  - Current state: {current_state}"
                f"    - Route: {current_state.route}"
                f"    - Time: {current_state_time}"
                f"  - Next state: {next_state}"
                f"    - Route: {next_state.route}"
                f"    - Time: {next_state_time}"
                f"  - Time difference: {time_diff}"
                f"  - Improvement: {time_diff * self.goal_evaluator.goal_type().value} -> {improvement > 0}"
            )
        )

        return improvement

    def evaluate(self, state: TripState):
        return self.goal_evaluator.evaluate(state)

    def process_solution(self, state: TripState) -> dict:
        return {
            "route": state.ordered_places_with_times(
                self.time_matrix,
                self.trip_params.firstDayTimestamp,
                self.trip_params.dayStartTimestamp,
            ),
            "geometry": state.path_multiline_string_by_days(),
        }

    def _initial_state(self) -> TripState:
        return TripState.initial_state(self.all_places, self.number_of_nights)

    def _calculate_time_matrix(self):
        pgr = PgRouting()

        # Calculate time matrix between all points
        time_matrix = pgr.get_time_matrix(self.all_places)

        # Add time to spend in each place horizontally to the matrix (0 for accommodation)
        time_to_spend = np.array(
            [
                feature.properties["timeToSpend"] * 60
                if "timeToSpend" in feature.properties
                else 0
                for feature in self.all_places.features
            ],
            dtype=np.float64,
        )
        time_matrix += time_to_spend

        return time_matrix
