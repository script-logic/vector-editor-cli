"""
Line segment entity implementation.
"""

from dataclasses import dataclass

from .shape import Coordinates, ShapeBase


@dataclass(frozen=True)
class Line(ShapeBase):
    """
    Represents a line segment between two points.

    A line has zero area (it's 1-dimensional) but has a
    non-zero length which serves as its perimeter.

    Attributes:
        start: Starting point coordinates
        end: Ending point coordinates
    """

    start: Coordinates
    end: Coordinates

    def __post_init__(self) -> None:
        """Validate that start and end points are different."""
        if self.start == self.end:
            raise ValueError("Start and end points must be different")

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Line(id={self.id}, "
            f"start=({self.start.x}, {self.start.y}), "
            f"end=({self.end.x}, {self.end.y}))"
        )
