from dataclasses import dataclass

from geojson import Point, loads


@dataclass
class WayVertex:
    id: int
    osm_id: int
    eout: int
    lon: float
    lat: float
    cnt: int
    chk: int
    ein: int
    the_geom: Point

    @classmethod
    def from_pgr(
        cls,
        id: int,
        osm_id: int,
        eout: int,
        lon: float,
        lat: float,
        cnt: int,
        chk: int,
        ein: int,
        the_geom: str,
    ) -> "WayVertex":
        geom = loads(the_geom)
        return cls(id, osm_id, eout, lon, lat, cnt, chk, ein, geom)

    def __str__(self):
        return f"""
            ID: {self.id},
            OSM ID: {self.osm_id},
            EOUT: {self.eout},
            Lon: {self.lon},
            Lat: {self.lat},
            CNT: {self.cnt},
            CHK: {self.chk},
            EIN: {self.ein},
            The_geom: {self.the_geom}
        """
