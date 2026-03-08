import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    """
    Immutable coordinates in 2D space.

    All geometric calculations return new Coordinates instances
    rather than modifying existing ones.
    """

    x: float
    y: float

    def rotate(self, angle_deg: float, center: Coordinates) -> Coordinates:
        """
        Rotate this point around a center point by given angle.

        Args:
            angle_deg: Rotation angle in degrees
            center: Center of rotation

        Returns:
            New rotated coordinates
        """
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        translated_x = self.x - center.x
        translated_y = self.y - center.y

        rotated_x = translated_x * cos_a - translated_y * sin_a
        rotated_y = translated_x * sin_a + translated_y * cos_a

        return Coordinates(
            x=rotated_x + center.x,
            y=rotated_y + center.y,
        )

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"Coordinates(x={self.x:.2f}, y={self.y:.2f})"
