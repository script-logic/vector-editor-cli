from dataclasses import dataclass

from src.vector_editor.domain.primitives import Coordinates

from .base import GeometryBase


@dataclass(frozen=True)
class PointGeometry(GeometryBase):
    """
    Geometric representation of a point.
    """

    coordinates: Coordinates

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"Point({self.coordinates.x:.2f}, {self.coordinates.y:.2f})"
