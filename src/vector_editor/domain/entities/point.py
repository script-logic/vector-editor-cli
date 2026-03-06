"""
Point entity implementation.
"""

from dataclasses import dataclass

from .shape import Coordinates, ShapeBase


@dataclass(frozen=True)
class Point(ShapeBase):
    """
    Represents a point in 2D space.

    A point has zero area and zero perimeter.
    It's the simplest geometric shape.

    Attributes:
        coordinates: The (x, y) coordinates of the point
    """

    coordinates: Coordinates

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Point(id={self.id}, "
            f"x={self.coordinates.x}, "
            f"y={self.coordinates.y})"
        )
