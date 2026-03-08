"""
In-memory implementation of shape repository.
"""

from uuid import UUID

from src.vector_editor.domain import PlacedShape
from src.vector_editor.domain.interfaces import IShapeRepository
from src.vector_editor.logger import get_logger

logger = get_logger(__name__)


class InMemoryShapeRepository(IShapeRepository):
    """
    Thread-safe in-memory implementation of shape repository.

    Stores shapes in a dictionary keyed by UUID. Shapes are lost
    when the application stops.
    """

    def __init__(self) -> None:
        """Initialize an empty repository."""
        self._shapes: dict[UUID, PlacedShape] = {}
        self._logger = logger.bind(component="InMemoryShapeRepository")

    def add(self, shape: PlacedShape) -> None:
        """
        Add a shape to the repository.

        Args:
            shape: The shape to add

        Raises:
            ValueError: If a shape with the same ID already exists
        """
        if shape.id in self._shapes:
            self._logger.error(
                "shape_already_exists",
                shape_id=str(shape.id),
            )
            raise ValueError(f"Shape with id {shape.id} already exists")

        self._shapes[shape.id] = shape
        self._logger.debug(
            "shape_added",
            shape_id=str(shape.id),
            shape_type=type(shape.definition).__name__,
            total_shapes=len(self._shapes),
        )

    def remove(self, shape_id: UUID) -> None:
        """
        Remove a shape by its ID.

        Args:
            shape_id: ID of the shape to remove

        Raises:
            KeyError: If no shape with the given ID exists
        """
        if shape_id not in self._shapes:
            self._logger.error(
                "shape_not_found_for_removal",
                shape_id=str(shape_id),
            )
            raise KeyError(f"Shape with id {shape_id} not found")

        shape_type = type(self._shapes[shape_id].definition).__name__
        del self._shapes[shape_id]
        self._logger.debug(
            "shape_removed",
            shape_id=str(shape_id),
            shape_type=shape_type,
            total_shapes=len(self._shapes),
        )

    def get(self, shape_id: UUID) -> PlacedShape | None:
        """
        Get a shape by its ID.

        Args:
            shape_id: ID of the shape to retrieve

        Returns:
            The shape if found, None otherwise
        """
        shape = self._shapes.get(shape_id)
        self._logger.debug(
            "shape_retrieved",
            shape_id=str(shape_id),
            found=shape is not None,
        )
        return shape

    def get_all(self) -> list[PlacedShape]:
        """
        Get all shapes in the repository.

        Returns:
            List of all shapes
        """
        shapes = list(self._shapes.values())
        self._logger.debug(
            "all_shapes_retrieved",
            count=len(shapes),
        )
        return shapes

    def clear(self) -> None:
        """Remove all shapes from the repository."""
        previous_count = len(self._shapes)
        self._shapes.clear()
        self._logger.debug(
            "repository_cleared",
            removed_count=previous_count,
        )

    def count(self) -> int:
        """
        Get the number of shapes in the repository.

        Returns:
            Total number of shapes
        """
        return len(self._shapes)
