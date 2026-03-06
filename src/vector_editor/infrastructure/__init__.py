"""
Infrastructure layer providing concrete implementations.
"""

from .repositories.memory_repository import InMemoryShapeRepository

__all__ = [
    "InMemoryShapeRepository",
]
