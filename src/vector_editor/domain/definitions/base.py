from abc import ABC, abstractmethod
from typing import Protocol

from src.vector_editor.domain.geometry import IShape
from src.vector_editor.domain.primitives import Transform


class IShapeDefinition(Protocol):
    """
    Protocol defining the interface for all shape definitions.

    A definition contains the essential parameters needed to create
    a shape (e.g., for a line: start point and end point, OR
    origin, length, and angle). It knows how to render itself into
    concrete geometry given a transform.
    """

    def to_geometry(self, transform: Transform) -> IShape:
        """
        Convert this definition to concrete geometry with given transform.

        Args:
            transform: Transformation to apply (rotation, etc.)

        Returns:
            Concrete geometric shape
        """
        ...


class ShapeDefinitionBase(ABC):
    """
    Base class for shape definitions providing common functionality.
    """

    @abstractmethod
    def to_geometry(self, transform: Transform) -> IShape:
        """Convert to geometry"""
