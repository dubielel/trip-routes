from pydantic import BaseModel
from geojson_pydantic import Feature, FeatureCollection, Point, MultiLineString


class CalculateTripResponse(BaseModel):
    route: list[FeatureCollection[Feature[Point, dict]]]
    geometry: Feature[MultiLineString, dict]
