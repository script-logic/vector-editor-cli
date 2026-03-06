"""
Circle entity implementation.
"""

from dataclasses import dataclass

from .shape import Coordinates, ShapeBase


@dataclass
class Circle(ShapeBase):
    """
    Represents a circle in 2D space.

    Attributes:
        center: Center point coordinates
        radius: Radius of the circle (must be positive)
    """

    center: Coordinates
    radius: float

    def __post_init__(self) -> None:
        """Initialize base class and validate radius."""
        super().__init__()
        if self.radius <= 0:
            raise ValueError(f"Radius must be positive, got {self.radius}")

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Circle(id={self.id}, "
            f"center=({self.center.x}, {self.center.y}), "
            f"radius={self.radius})"
        )
