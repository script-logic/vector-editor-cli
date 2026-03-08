from dataclasses import dataclass

from src.vector_editor.domain.geometry import EllipseGeometry
from src.vector_editor.domain.primitives import Coordinates, Transform

from .base import ShapeDefinitionBase


@dataclass(frozen=True)
class EllipseDefinition(ShapeDefinitionBase):
    """
    An ellipse is defined by its center, horizontal radius (x-radius),
    and vertical radius (y-radius).
    """

    center: Coordinates
    radius_x: float
    radius_y: float

    def __post_init__(self) -> None:
        """Validate radii."""
        if self.radius_x <= 0:
            raise ValueError(f"X-radius must be positive, got {self.radius_x}")
        if self.radius_y <= 0:
            raise ValueError(f"Y-radius must be positive, got {self.radius_y}")

    def to_geometry(self, transform: Transform) -> EllipseGeometry:
        """
        Convert ellipse definition to concrete geometry with given rotation.

        The ellipse rotates around its center.
        """
        return EllipseGeometry(
            center=self.center,
            radius_x=self.radius_x,
            radius_y=self.radius_y,
            rotation_deg=transform.rotation_deg,
        )
