from abc import ABC
from typing import Protocol


class IShape(Protocol):
    """
    Protocol defining the interface for all geometric shapes.

    Geometry objects are pure data containers without identity.
    """

    def __str__(self) -> str:
        """Human-readable representation."""
        ...


class GeometryBase(ABC):
    """
    Abstract base class for geometric shapes.
    """
