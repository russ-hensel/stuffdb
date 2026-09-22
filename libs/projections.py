"""Pixel <-> (lat, lon) projection strategies.

Pure-Python; no Qt dependency so this module is trivial to unit-test.
All projections cover the whole world: lon in [-180, 180], lat in [-90, 90].
"""
from __future__ import annotations

from typing import Protocol


#----------------------------------
class Projection(Protocol):
    """Strategy interface for converting between pixmap pixels and degrees."""

    width:  int
    height: int

    def pixel_to_latlon(self, x: float, y: float) -> tuple[float, float]: ...
    def latlon_to_pixel(self, lat: float, lon: float) -> tuple[float, float]: ...
    def in_bounds(self, x: float, y: float) -> bool: ...


#----------------------------------
class EquirectangularProjection:
    """Plate Carrée: x is linear in longitude, y is linear in latitude.

    The pixmap origin (0, 0) is the top-left, i.e. (lat=+90, lon=-180).
    """

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(
                f"width and height must be positive (got {width}x{height})"
            )
        self.width  = int(width)
        self.height = int(height)

    def pixel_to_latlon(self, x: float, y: float) -> tuple[float, float]:
        lon = (x / self.width)  * 360.0 - 180.0
        lat =  90.0 - (y / self.height) * 180.0
        return lat, lon

    def latlon_to_pixel(self, lat: float, lon: float) -> tuple[float, float]:
        x = (lon + 180.0) / 360.0 * self.width
        y = ( 90.0 - lat) / 180.0 * self.height
        return x, y

    def in_bounds(self, x: float, y: float) -> bool:
        return 0.0 <= x <= self.width and 0.0 <= y <= self.height

# ---- eof
