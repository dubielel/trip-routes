from dataclasses import dataclass


@dataclass
class Point:
    longitude: float
    latitude: float

    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f"(Lon: {self.longitude}, Lat: {self.latitude})"
