from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .definitions import IShapeDefinition
from .geometry import IShape
from .primitives import Transform


@dataclass
class PlacedShape:
    """
    A shape placed in the world with a specific transform.

    This is what the repository stores. It contains:
    - A unique ID
    - The shape definition (how the shape was created)
    - The transform (rotation, etc.)

    The actual geometry is computed on-demand by calling render().
    """

    definition: IShapeDefinition
    transform: Transform = field(
        default_factory=lambda: Transform(rotation_deg=0)
    )
    id: UUID = field(default_factory=uuid4)

    def render(self) -> IShape:
        """
        Compute the concrete geometry for this shape.

        Returns:
            Geometric representation with current transform applied
        """
        return self.definition.to_geometry(self.transform)

    def with_rotation(self, angle_deg: float) -> PlacedShape:
        """
        Create a new PlacedShape with updated rotation.

        Args:
            angle_deg: New rotation angle

        Returns:
            New PlacedShape instance (immutable transform)
        """
        return PlacedShape(
            definition=self.definition,
            transform=Transform(rotation_deg=angle_deg),
            id=self.id,
        )
