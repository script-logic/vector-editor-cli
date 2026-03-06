"""
Square entity implementation.
"""

from dataclasses import dataclass

from .shape import Coordinates, ShapeBase


@dataclass
class Square(ShapeBase):
    """
    Represents a square aligned with coordinate axes.

    The square is defined by its top-left corner and side length,
    with sides parallel to the X and Y axes.

    Attributes:
        top_left: Top-left corner coordinates
        side_length: Length of each side (must be positive)
    """

    top_left: Coordinates
    side_length: float

    def __post_init__(self) -> None:
        """Initialize base class and validate side length."""
        super().__init__()
        if self.side_length <= 0:
            raise ValueError(
                f"Side length must be positive, got {self.side_length}"
            )

    def bottom_right(self) -> Coordinates:
        """Calculate the bottom-right corner coordinates."""
        return Coordinates(
            x=self.top_left.x + self.side_length,
            y=self.top_left.y + self.side_length,
        )

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Square(id={self.id}, "
            f"top_left=({self.top_left.x}, {self.top_left.y}), "
            f"side={self.side_length})"
        )
