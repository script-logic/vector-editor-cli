from dataclasses import dataclass

from src.vector_editor.domain.primitives import Coordinates

from .base import GeometryBase


@dataclass(frozen=True)
class LineGeometry(GeometryBase):
    """
    Geometric representation of a line segment.
    """

    start: Coordinates
    end: Coordinates

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Line({self.start.x:.2f}, {self.start.y:.2f}) → "
            f"({self.end.x:.2f}, {self.end.y:.2f})"
        )
