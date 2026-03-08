from dataclasses import dataclass

from src.vector_editor.domain.geometry import CircleGeometry
from src.vector_editor.domain.primitives import Coordinates, Transform

from .base import ShapeDefinitionBase


@dataclass(frozen=True)
class CircleDefinition(ShapeDefinitionBase):
    """
    A circle is defined by its center and radius.
    When rotated around its center, a circle remains unchanged.
    """

    center: Coordinates
    radius: float

    def __post_init__(self) -> None:
        """Validate radius."""
        if self.radius <= 0:
            raise ValueError(f"Radius must be positive, got {self.radius}")

    def to_geometry(self, transform: Transform) -> CircleGeometry:
        """
        Convert circle definition to concrete geometry.
        """
        rotated_center = self.center.rotate(
            transform.rotation_deg,
            center=self.center,
        )
        return CircleGeometry(
            center=rotated_center,
            radius=self.radius,
        )
