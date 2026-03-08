"""
Domain layer for the vector editor.

This package follows clean architecture principles and contains:
- Primitives: Basic geometric building blocks
- Definitions: Shape creation parameters
- Geometry: Computed geometric representations
- PlacedShape: Container for definitions with transforms
"""

from . import definitions, geometry, primitives
from .placed_shape import PlacedShape

__all__ = [
    "PlacedShape",
    "definitions",
    "geometry",
    "primitives",
]
