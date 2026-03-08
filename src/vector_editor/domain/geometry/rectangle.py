from dataclasses import dataclass

from src.vector_editor.domain.primitives import Coordinates

from .base import GeometryBase


@dataclass(frozen=True)
class RectangleGeometry(GeometryBase):
    """
    Geometric representation of a rectangle.
    """

    top_left: Coordinates
    top_right: Coordinates
    bottom_right: Coordinates
    bottom_left: Coordinates
    center: Coordinates
    width: float
    height: float

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Rectangle(center=({self.center.x:.2f}, {self.center.y:.2f}), "
            f"width={self.width:.2f}, height={self.height:.2f})"
        )
