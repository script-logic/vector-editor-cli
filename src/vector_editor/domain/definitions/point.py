from dataclasses import dataclass

from src.vector_editor.domain.geometry import PointGeometry
from src.vector_editor.domain.primitives import Coordinates, Transform

from .base import ShapeDefinitionBase


@dataclass(frozen=True)
class PointDefinition(ShapeDefinitionBase):
    """
    A point is defined by its coordinates. When transformed,
    the point rotates around itself.
    """

    coordinates: Coordinates

    def to_geometry(self, transform: Transform) -> PointGeometry:
        """
        Convert point definition to concrete geometry.
        """
        rotated_coords = self.coordinates.rotate(
            transform.rotation_deg,
            center=self.coordinates,
        )
        return PointGeometry(coordinates=rotated_coords)
