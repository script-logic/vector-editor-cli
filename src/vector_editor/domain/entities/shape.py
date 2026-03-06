"""
Base abstractions and common types for geometric shapes.
"""

from abc import ABC
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Coordinates:
    """
    Coordinates in 2D space.

    Attributes:
        x: X-coordinate
        y: Y-coordinate
    """

    x: float
    y: float


class Shape(Protocol):
    """
    Protocol defining the interface for all geometric shapes.
    """

    @property
    def id(self) -> UUID:
        """Unique identifier of the shape."""
        ...


class ShapeBase(ABC):
    """
    Abstract base class providing common functionality for shapes.
    """

    def __init__(self) -> None:
        self._id = uuid4()

    @property
    def id(self) -> UUID:
        return self._id
