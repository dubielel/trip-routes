import logging

import numpy as np
import numpy.typing as npt
from datetime import datetime, timedelta
from copy import deepcopy
from random import shuffle

from geojson_pydantic import (
    Feature,
    FeatureCollection,
    Point,
    MultiLineString,
    LineString,
)

from pgrouting.PgRouting import PgRouting
from pgrouting.PathPart import PathPart

from utils.hex_color import get_hex_colors

logger = logging.getLogger(__name__)


class TripState:
    def __init__(
        self,
        all_places: FeatureCollection[Feature[Point, dict]],
        route: list[int],
    ):
        self.all_places = all_places
        """
        All places to visit including accommodation at the beginning of the list
        """
        self.route = tuple(route)
        """
        List of indices of places in the order of visit in this state
        """

        logger.info(f"Initialized TripState with route: {self.route}")

    def __str__(self):
        return " -> ".join(
            self.all_places.features[index].properties["displayName"]
            for index in self.route
        )

    def __eq__(self, other):
        if not isinstance(other, TripState):
            return False
        return self.route == other.route

    def __hash__(self):
        return hash(self.route)

    @staticmethod
    def _init_route(
        all_places: FeatureCollection[Feature[Point, dict]],
        number_of_nights: int,
    ):
        """
        Initialize route with accommodation placed on the beginning,
        between places that many times as the number of nights and at the end of the route
        """

        accommodation_index = 0
        number_of_accommodations = number_of_nights + 2
        places_to_visit_length = len(all_places.features) - 1
        route_length = places_to_visit_length + number_of_accommodations

        accommodation_in_route_indices = (
            np.linspace(0, route_length - 1, number_of_accommodations)
            .round()
            .astype(int)
            .tolist()
        )

        initial_route = list(range(1, len(all_places.features)))

        for route_index in accommodation_in_route_indices:
            initial_route.insert(route_index, accommodation_index)

        return initial_route

    @staticmethod
    def _init_random_route(
        all_places: FeatureCollection[Feature[Point, dict]],
        number_of_nights: int,
    ):
        """
        Initialize random route with accommodation placed on the beginning,
        between places that many times as the number of nights and at the end of the route
        """

        initial_route = TripState._init_route(all_places, number_of_nights)

        first = initial_route[0]
        last = initial_route[-1]
        middle = initial_route[1:-1]
        shuffle(middle)

        return [first] + middle + [last]

    @classmethod
    def initial_state(
        cls,
        all_places: FeatureCollection[Feature[Point, dict]],
        number_of_nights: int,
    ):
        initial_route = cls._init_route(all_places, number_of_nights)
        return cls(all_places, initial_route)

    @classmethod
    def random_state(
        cls,
        all_places: FeatureCollection[Feature[Point, dict]],
        number_of_nights: int,
    ):
        random_route = cls._init_random_route(all_places, number_of_nights)
        return cls(all_places, random_route)

    def ordered_places_with_times(
        self,
        time_matrix: npt.NDArray[np.float64],
        first_day_timestamp: int,
        start_day_timestamp: int,
    ) -> list[FeatureCollection[Feature[Point, dict]]]:
        first_day = datetime.fromtimestamp(first_day_timestamp // 1000)
        start_day = first_day + timedelta(
            hours=datetime.fromtimestamp(start_day_timestamp // 1000).hour
        )

        days_route = self._divide_route_into_days()

        ordered_places: list[FeatureCollection[Feature[Point, dict]]] = []
        for day in days_route:
            day_places = [
                deepcopy(self.all_places.features[place_index]) for place_index in day
            ]

            if all(place_index == 0 for place_index in day):
                for i in range(len(day_places)):
                    day_places[i].properties["departureTimestamp"] = None
                    day_places[i].properties["arrivalTimestamp"] = None
                ordered_places.append(
                    FeatureCollection(
                        type="FeatureCollection",
                        features=day_places,
                    )
                )
                start_day += timedelta(days=1)
                continue

            day_places_index = 0
            day_places[0].properties["departureTimestamp"] = (
                start_day.timestamp() * 1000
            )
            day_places[0].properties["arrivalTimestamp"] = None
            day_places_index += 1

            for start_place_index, end_place_index in zip(day[:-1], day[1:]):
                time_1 = time_matrix[start_place_index][end_place_index]
                time_2 = time_1 - time_matrix[end_place_index][end_place_index]

                if end_place_index == 0:
                    day_places[day_places_index].properties["departureTimestamp"] = None
                else:
                    day_places[day_places_index].properties["departureTimestamp"] = (
                        day_places[day_places_index - 1].properties[
                            "departureTimestamp"
                        ]
                        + time_1 * 1000
                    )
                day_places[day_places_index].properties["arrivalTimestamp"] = (
                    day_places[day_places_index - 1].properties["departureTimestamp"]
                    + time_2 * 1000
                )
                day_places_index += 1

            ordered_places.append(
                FeatureCollection(
                    type="FeatureCollection",
                    features=day_places,
                )
            )
            start_day += timedelta(days=1)


        return ordered_places

    def path_multiline_string_by_days(self) -> Feature[MultiLineString, dict]:
        pgr = PgRouting()

        day_routes = self._divide_route_into_days()
        line_strings: list[LineString] = []

        for day_route in day_routes:
            logger.info(f"Day route: {day_route}")
            day_line_strings: list[LineString] = []
            for start_place_index, end_place_index in zip(
                day_route[:-1], day_route[1:]
            ):
                logger.info(
                    f"Start place index: {start_place_index}, end place index: {end_place_index}"
                )
                start_place = self.all_places.features[start_place_index]
                end_place = self.all_places.features[end_place_index]

                line_string = pgr.get_linestring_path(
                    start_place.geometry, end_place.geometry
                )
                logger.info(
                    f"Line string start: {line_string.coordinates[0]}, end: {line_string.coordinates[-1]}"
                )
                if line_string is not None:
                    day_line_strings.append(line_string)

            all_day_coords = []
            for line_string in day_line_strings:
                all_day_coords.extend(line_string.coordinates)
            line_strings.append(
                LineString(
                    type="LineString",
                    coordinates=all_day_coords,
                )
            )

        return Feature(
            type="Feature",
            geometry=MultiLineString(
                type="MultiLineString",
                coordinates=[line_string.coordinates for line_string in line_strings],
            ),
            properties={"colors": get_hex_colors(n=len(line_strings))},
        )

    def _divide_route_into_days(self) -> list[list[int]]:
        """
        Divide the route into days
        """

        days: list[list[int]] = []
        current_accommodation_index = 0
        while current_accommodation_index < len(self.route) - 1:
            next_accommodation_index = self.route.index(
                0, current_accommodation_index + 1
            )

            day_trip = self.route[
                current_accommodation_index : next_accommodation_index + 1
            ]
            days.append(day_trip)

            current_accommodation_index = next_accommodation_index

        return days

    def ordered_places(self) -> list[Feature[Point, dict]]:
        return [self.all_places.features[index] for index in self.route]

    def paths_between_places(self) -> list[list[PathPart]]:
        pgr = PgRouting()

        paths_between_places: list[list[PathPart]] = []

        for start_place_index, end_place_index in zip(self.route[:-1], self.route[1:]):
            start_place = self.all_places.features[start_place_index]
            end_place = self.all_places.features[end_place_index]

            path = pgr.get_shortest_path(start_place.geometry, end_place.geometry)
            paths_between_places.append(path)

        return paths_between_places

    def path_multiline_string(self) -> MultiLineString:
        pgr = PgRouting()

        line_strings: list[LineString] = []
        for start_place_index, end_place_index in zip(self.route[:-1], self.route[1:]):
            start_place = self.all_places.features[start_place_index]
            end_place = self.all_places.features[end_place_index]

            line_string = pgr.get_linestring_path(
                start_place.geometry, end_place.geometry
            )
            if line_string is not None:
                line_strings.append(line_string)

        return MultiLineString(
            type="MultiLineString",
            coordinates=[line_string.coordinates for line_string in line_strings],
        )
