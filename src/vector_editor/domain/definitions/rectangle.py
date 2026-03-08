from dataclasses import dataclass

from src.vector_editor.domain.geometry import RectangleGeometry
from src.vector_editor.domain.primitives import Coordinates, Transform

from .base import ShapeDefinitionBase


@dataclass(frozen=True)
class RectangleDefinition(ShapeDefinitionBase):
    """
    A rectangle is defined by its center, width, and height.
    """

    center: Coordinates
    width: float
    height: float

    def __post_init__(self) -> None:
        """Validate dimensions."""
        if self.width <= 0:
            raise ValueError(f"Width must be positive, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"Height must be positive, got {self.height}")

    def to_geometry(self, transform: Transform) -> RectangleGeometry:
        """
        Convert rectangle definition to concrete geometry with given rotation.

        The rectangle rotates around its center.
        """
        half_w = self.width / 2
        half_h = self.height / 2

        local_corners = [
            Coordinates(x=-half_w, y=-half_h),
            Coordinates(x=half_w, y=-half_h),
            Coordinates(x=half_w, y=half_h),
            Coordinates(x=-half_w, y=half_h),
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

        return RectangleGeometry(
            top_left=world_corners[0],
            top_right=world_corners[1],
            bottom_right=world_corners[2],
            bottom_left=world_corners[3],
            center=self.center,
            width=self.width,
            height=self.height,
        )
