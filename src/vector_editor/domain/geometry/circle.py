from dataclasses import dataclass

from src.vector_editor.domain.primitives import Coordinates

from .base import GeometryBase


@dataclass(frozen=True)
class CircleGeometry(GeometryBase):
    """
    Geometric representation of a circle.
    """

    center: Coordinates
    radius: float

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Circle(center=({self.center.x:.2f}, {self.center.y:.2f}), "
            f"radius={self.radius:.2f})"
        )
