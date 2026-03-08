import math
from dataclasses import dataclass
from enum import Enum

from src.vector_editor.domain.geometry import IShape, LineGeometry
from src.vector_editor.domain.primitives import Coordinates, Transform

from .base import ShapeDefinitionBase


class LineRepresentation(Enum):
    """How the line was originally defined."""

    TWO_POINTS = "two_points"
    POLAR = "polar"


@dataclass(frozen=True)
class LineDefinition(ShapeDefinitionBase):
    """
    Definition of a line segment.

    A line can be defined in two ways:
    1. By two endpoints (start, end)
    2. By origin, length, and angle (polar coordinates)

    The representation enum indicates which way was used,
    which is useful for UI and for maintaining the original intent.
    """

    representation: LineRepresentation

    start: Coordinates | None = None
    end: Coordinates | None = None

    origin: Coordinates | None = None
    length: float | None = None
    angle_deg: float | None = None

    def __post_init__(self) -> None:
        """Validate that the correct fields are provided."""
        if self.representation == LineRepresentation.TWO_POINTS:
            if self.start is None or self.end is None:
                raise ValueError(
                    "Two-point representation requires start and end"
                )
            if self.start == self.end:
                raise ValueError("Start and end points must be different")

        elif self.representation == LineRepresentation.POLAR:
            if (
                self.origin is None
                or self.length is None
                or self.angle_deg is None
            ):
                raise ValueError(
                    "Polar representation requires origin, length, and angle"
                )
            if self.length <= 0:
                raise ValueError(f"Length must be positive, got {self.length}")

    @classmethod
    def from_points(
        cls, start: Coordinates, end: Coordinates
    ) -> LineDefinition:
        """
        Create a line definition from two endpoints.
        """
        return cls(
            representation=LineRepresentation.TWO_POINTS,
            start=start,
            end=end,
        )

    @classmethod
    def from_polar(
        cls,
        origin: Coordinates,
        length: float,
        angle_deg: float,
    ) -> LineDefinition:
        """
        Create a line definition from polar coordinates.

        Args:
            origin: Starting point
            length: Length of the line
            angle_deg: Direction angle in degrees
        """
        return cls(
            representation=LineRepresentation.POLAR,
            origin=origin,
            length=length,
            angle_deg=angle_deg % 360,
        )

    def to_geometry(self, transform: Transform) -> IShape:
        """
        Convert line definition to concrete geometry with given rotation.

        For two-point lines, we rotate both points around the line's center.
        For polar lines, we add the transform's rotation to the base angle.
        """
        if self.representation == LineRepresentation.TWO_POINTS:
            return self._two_points_to_geometry(transform)
        else:
            return self._polar_to_geometry(transform)

    def _two_points_to_geometry(self, transform: Transform) -> LineGeometry:
        """Convert two-point representation with rotation."""
        if self.start is None or self.end is None:
            raise ValueError("Two-point representation requires start and end")
        center = Coordinates(
            x=(self.start.x + self.end.x) / 2,
            y=(self.start.y + self.end.y) / 2,
        )

        rotated_start = self.start.rotate(transform.rotation_deg, center)
        rotated_end = self.end.rotate(transform.rotation_deg, center)

        return LineGeometry(start=rotated_start, end=rotated_end)

    def _polar_to_geometry(self, transform: Transform) -> LineGeometry:
        """Convert polar representation with rotation."""
        if (
            self.origin is None
            or self.length is None
            or self.angle_deg is None
        ):
            raise ValueError(
                "Polar representation requires origin, length, and angle"
            )

        total_angle_deg = (self.angle_deg + transform.rotation_deg) % 360
        angle_rad = math.radians(total_angle_deg)

        dx = self.length * math.cos(angle_rad)
        dy = self.length * math.sin(angle_rad)

        end_point = Coordinates(
            x=self.origin.x + dx,
            y=self.origin.y + dy,
        )

        return LineGeometry(start=self.origin, end=end_point)
