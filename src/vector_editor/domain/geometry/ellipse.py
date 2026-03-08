from dataclasses import dataclass

from src.vector_editor.domain.primitives import Coordinates

from .base import GeometryBase


@dataclass(frozen=True)
class EllipseGeometry(GeometryBase):
    """
    Geometric representation of an ellipse (rotated if needed).
    """

    center: Coordinates
    radius_x: float
    radius_y: float
    rotation_deg: float

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Ellipse(center=({self.center.x:.2f}, {self.center.y:.2f}), "
            f"rx={self.radius_x:.2f}, ry={self.radius_y:.2f}, "
            f"rotation={self.rotation_deg:.1f}°)"
        )
