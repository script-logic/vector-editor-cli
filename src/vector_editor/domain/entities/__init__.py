"""
Domain entities for the vector editor.

This package contains all geometric shapes and related data structures.
"""

from .circle import Circle
from .line import Line
from .point import Point
from .shape import Coordinates, IShape, ShapeBase
from .square import Square

__all__ = [
    "Circle",
    "Coordinates",
    "IShape",
    "Line",
    "Point",
    "ShapeBase",
    "Square",
]
