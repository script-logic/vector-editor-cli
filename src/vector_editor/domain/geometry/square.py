from dataclasses import dataclass

from src.vector_editor.domain.primitives import Coordinates

from .base import GeometryBase


@dataclass(frozen=True)
class SquareGeometry(GeometryBase):
    """
    Geometric representation of a square.
    """

    top_left: Coordinates
    top_right: Coordinates
    bottom_right: Coordinates
    bottom_left: Coordinates
    center: Coordinates
    side_length: float

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Square(center=({self.center.x:.2f}, {self.center.y:.2f}), "
            f"side={self.side_length:.2f})"
        )
