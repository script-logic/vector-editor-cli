"""
Repository interfaces for shape storage.
"""

from typing import Protocol
from uuid import UUID

from src.vector_editor.domain.entities import Shape


class IShapeRepository(Protocol):
    """
    Protocol defining the interface for shape storage.

    This follows the Repository pattern, providing a collection-like
    interface for accessing shapes without exposing storage details.
    """

    def add(self, shape: Shape) -> None:
        """Add a shape to the repository."""
        ...

    def remove(self, shape_id: UUID) -> None:
        """Remove a shape by its ID."""
        ...

    def get(self, shape_id: UUID) -> Shape | None:
        """Get a shape by its ID, returns None if not found."""
        ...

    def get_all(self) -> list[Shape]:
        """Get all shapes in the repository."""
        ...

    def clear(self) -> None:
        """Remove all shapes from the repository."""
        ...

    def count(self) -> int:
        """Return the number of shapes in the repository."""
        ...
