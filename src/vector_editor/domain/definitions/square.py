from dataclasses import dataclass

from src.vector_editor.domain.geometry import SquareGeometry
from src.vector_editor.domain.primitives import Coordinates, Transform

from .base import ShapeDefinitionBase


@dataclass(frozen=True)
class SquareDefinition(ShapeDefinitionBase):
    """
    A square is defined by its center and side length.
    """

    center: Coordinates
    side_length: float

    def __post_init__(self) -> None:
        """Validate side length."""
        if self.side_length <= 0:
            raise ValueError(
                f"Side length must be positive, got {self.side_length}"
            )

    def to_geometry(self, transform: Transform) -> SquareGeometry:
        """
        Convert square definition to concrete geometry with given rotation.

        The square rotates around its center.
        """
        half = self.side_length / 2

        local_corners = [
            Coordinates(x=-half, y=-half),
            Coordinates(x=half, y=-half),
            Coordinates(x=half, y=half),
            Coordinates(x=-half, y=half),
        ]

        rotated_corners = [
            corner.rotate(transform.rotation_deg, Coordinates(x=0, y=0))
            for corner in local_corners
        ]

        world_corners = [
            Coordinates(
                x=self.center.x + corner.x,
                y=self.center.y + corner.y,
            )
            for corner in rotated_corners
        ]

        return SquareGeometry(
            top_left=world_corners[0],
            top_right=world_corners[1],
            bottom_right=world_corners[2],
            bottom_left=world_corners[3],
            center=self.center,
            side_length=self.side_length,
        )
