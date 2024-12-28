from pydantic import BaseModel
from geojson_pydantic import Feature, FeatureCollection, Point


class CalculateTripRequestBody(BaseModel):
    firstDayTimestamp: int
    lastDayTimestamp: int
    accommodation: Feature[Point, dict]
    dayStartTimestamp: int
    dayEndTimestamp: int
    placesToVisit: FeatureCollection[Feature[Point, dict]]
