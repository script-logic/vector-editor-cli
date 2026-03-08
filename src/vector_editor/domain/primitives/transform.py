from dataclasses import dataclass


@dataclass(frozen=True)
class Transform:
    """
    Transformation applied to a shape definition.
    """

    rotation_deg: float

    def __post_init__(self) -> None:
        """Normalize rotation to [0, 360) range."""
        normalized = self.rotation_deg % 360
        object.__setattr__(self, "rotation_deg", normalized)

    @property
    def rotation_rad(self) -> float:
        """Rotation in radians (for calculations)."""
        import math

        return math.radians(self.rotation_deg)
