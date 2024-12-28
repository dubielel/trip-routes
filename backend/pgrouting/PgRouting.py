import logging

import psycopg2 as pg
from geojson_pydantic import Point, FeatureCollection, Feature, LineString
import geojson

import numpy as np
import numpy.typing as npt
from math import isclose

from models.WayVertex import WayVertex
from models.PathPart import PathPart

logger = logging.getLogger(__name__)


DATABASE = "routing"
HOST = "localhost"
PORT = "5432"
USER = "postgres"
PASSWORD = "postgres"

SRID = 4326

DEFAULT_REL_TOL = (
    1e-6  # because of the precision of the geojson coordinates (6 decimal places)
)


class PgRouting:
    def __init__(self):
        self.conn = pg.connect(
            database=DATABASE,
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
        )
        self.cursor = self.conn.cursor()

    def get_time_matrix(
        self, places: FeatureCollection[Feature[Point, dict]]
    ) -> npt.NDArray[np.float64]:
        places_vertices: list[WayVertex] = []
        for place in places.features:
            vertex = self._get_nearest_way_vertex(place.geometry)
            places_vertices.append(vertex)

        self.cursor.execute(f"""
            SELECT
                *
            FROM pgr_bdAstarCostMatrix(
                '
                    SELECT
                        gid AS id,
                        source,
                        target,
                        cost_s AS cost,
                        reverse_cost_s AS reverse_cost,
                        x1,
                        y1,
                        x2,
                        y2
                    FROM ways
                ',
                (
                    SELECT array_agg(id)
                    FROM ways_vertices_pgr
                    WHERE id IN (
                        {', '.join(str(vertex.id) for vertex in places_vertices)}
                    )
                )
            );
        """)

        times = self.cursor.fetchall()  # start_vid, end_vid, agg_cost

        time_matrix = np.empty(
            (len(places.features), len(places.features)), dtype=float
        )

        for start_vertex_idx, end_vertex_idx, cost in times:
            start_idx = next(
                (
                    i
                    for i, vertex in enumerate(places_vertices)
                    if vertex.id == start_vertex_idx
                ),
                -1,
            )
            end_idx = next(
                (
                    i
                    for i, vertex in enumerate(places_vertices)
                    if vertex.id == end_vertex_idx
                ),
                -1,
            )
            time_matrix[start_idx][end_idx] = cost

        return time_matrix

    def get_linestring_path(self, start: Point, end: Point) -> LineString | None:
        if (
            start.coordinates[0] == end.coordinates[0]
            and start.coordinates[1] == end.coordinates[1]
        ):
            logger.info(f"Start point and end point are the same: {start}")
            return LineString(
                type="LineString",
                coordinates=[start.coordinates, end.coordinates],
            )

        start_vertex = self._get_nearest_way_vertex(start)
        end_vertex = self._get_nearest_way_vertex(end)

        self.cursor.execute(f"""
            SELECT
                ST_AsGeoJSON(
                    ST_LineMerge(
                        ST_Collect(
                            ST_Transform(edges.the_geom, 4326)
                        )
                    )
                )
            FROM pgr_bdAstar(
                '
                    SELECT
                        gid AS id, source, target, cost, reverse_cost, x1, y1, x2, y2
                    FROM ways
                ',
                {start_vertex.id},
                {end_vertex.id},
                directed => true,
                heuristic => 2
            ) AS path
            LEFT JOIN
                ways AS edges
            ON
                path.edge = edges.gid
            ;
        """)

        path_geojson_str: str | None = self.cursor.fetchone()[0]

        if logger.getEffectiveLevel() == logging.DEBUG:
            with open(f"path-{start_vertex.id}-{end_vertex.id}.json", "w") as fp:
                fp.write(path_geojson_str)

        if path_geojson_str is None:
            return None

        path_geojson: geojson.LineString = geojson.loads(path_geojson_str)

        # Path is reversed for some weird reason
        # (due to the way the ST_LineMerge function works with lines in different directions)
        #  Let's reverse it back
        if all(
            [
                isclose(
                    path_geojson["coordinates"][0][0],
                    end_vertex.lon,
                    rel_tol=DEFAULT_REL_TOL,
                ),
                isclose(
                    path_geojson["coordinates"][0][1],
                    end_vertex.lat,
                    rel_tol=DEFAULT_REL_TOL,
                ),
                isclose(
                    path_geojson["coordinates"][-1][0],
                    start_vertex.lon,
                    rel_tol=DEFAULT_REL_TOL,
                ),
                isclose(
                    path_geojson["coordinates"][-1][1],
                    start_vertex.lat,
                    rel_tol=DEFAULT_REL_TOL,
                ),
            ]
        ):
            path_geojson["coordinates"].reverse()

        try:
            return LineString(
                type=path_geojson["type"],
                coordinates=path_geojson["coordinates"],
            )
        except Exception as e:
            logger.error(
                f"Error while creating LineString path between points: {start} -> {end}: {e}"
            )
            return None

    def _get_nearest_way_vertex(self, point: Point) -> WayVertex:
        self.cursor.execute(f"""
            SELECT
                id,
                osm_id,
                eout,
                lon,
                lat,
                cnt,
                chk,
                ein,
                ST_AsGeoJSON(the_geom)
            FROM ways_vertices_pgr
            ORDER BY the_geom <-> ST_SetSRID(
                ST_MakePoint({point.coordinates[0]}, {point.coordinates[1]}),
                {SRID}
            )
            LIMIT 1;
        """)

        nearest_vertex = self.cursor.fetchone()
        if not nearest_vertex:
            raise ValueError(f"No nearest vertex found for point: {point}")

        return WayVertex.from_pgr(*nearest_vertex)

    def get_shortest_path(self, start: Point, end: Point) -> list[PathPart]:
        if (
            start.coordinates[0] == end.coordinates[0]
            and start.coordinates[1] == end.coordinates[1]
        ):
            logger.info(f"Start point and end point are the same: {start}")
            return []

        start_vertex = self._get_nearest_way_vertex(start)
        end_vertex = self._get_nearest_way_vertex(end)

        self.cursor.execute(f"""
            SELECT
                *
            FROM pgr_dijkstra(
                '
                    SELECT
                        gid AS id,
                        source,
                        target,
                        cost,
                        reverse_cost
                    FROM ways
                ',
                {start_vertex.id},
                {end_vertex.id},
                directed:=true
            );
        """)

        path = self.cursor.fetchall()
        if not path:
            raise ValueError(f"No path found between {start} and {end}")

        return [PathPart.from_pgr(*part) for part in path]

    def get_linestring_path_old(self, start: Point, end: Point) -> LineString | None:
        if (
            start.coordinates[0] == end.coordinates[0]
            and start.coordinates[1] == end.coordinates[1]
        ):
            logger.info(f"Start point and end point are the same: {start}")
            return LineString(
                type="LineString",
                coordinates=[start.coordinates, end.coordinates],
            )

        start_vertex = self._get_nearest_way_vertex(start)
        end_vertex = self._get_nearest_way_vertex(end)

        self.cursor.execute(f"""
            SELECT
                vertices.lon,
                vertices.lat
            FROM pgr_bdAstar(
                '
                    SELECT
                        gid AS id,
                        source,
                        target,
                        cost,
                        reverse_cost,
                        x1, y1,
                        x2, y2
                    FROM ways
                ',
                {start_vertex.id},
                {end_vertex.id},
                directed => true,
                heuristic => 2
            ) AS path
            LEFT JOIN
                ways_vertices_pgr AS vertices
            ON
                path.node = vertices.id
            ;
        """)

        points = self.cursor.fetchall()  # list[tuple[Decimal, Decimal]]

        try:
            return LineString(
                type="LineString",
                coordinates=[(float(lon), float(lat)) for lon, lat in points],
            )
        except Exception as e:
            logger.error(
                f"Error while creating LineString path between points: {start} -> {end}: {e}"
            )
            return None
