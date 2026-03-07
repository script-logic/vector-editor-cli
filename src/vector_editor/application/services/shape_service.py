"""
Application service for shape management.
"""

from uuid import UUID

from src.vector_editor.domain.entities import (
    Circle,
    Coordinates,
    IShape,
    Line,
    Point,
    Square,
)
from src.vector_editor.domain.interfaces import IShapeRepository
from src.vector_editor.logger import get_logger

logger = get_logger(__name__)


class ShapeService:
    """
    Application service coordinating shape operations.

    This service encapsulates the business logic for shape management
    and acts as a facade for the CLI layer.
    """

    def __init__(self, repository: IShapeRepository) -> None:
        """
        Initialize the service with a repository.

        Args:
            repository: The shape repository to use
        """
        self._repository = repository
        self._logger = logger.bind(component="ShapeService")

    def create_point(self, x: float, y: float) -> Point:
        """
        Create and store a new point.

        Args:
            x: X-coordinate
            y: Y-coordinate

        Returns:
            The created point
        """
        point = Point(coordinates=Coordinates(x=x, y=y))
        self._repository.add(point)
        self._logger.debug(
            "point_created",
            shape_id=str(point.id),
            x=x,
            y=y,
        )
        return point

    def create_line(self, x1: float, y1: float, x2: float, y2: float) -> Line:
        """
        Create and store a new line segment.

        Args:
            x1: Start point X-coordinate
            y1: Start point Y-coordinate
            x2: End point X-coordinate
            y2: End point Y-coordinate

        Returns:
            The created line
        """
        line = Line(
            start=Coordinates(x=x1, y=y1),
            end=Coordinates(x=x2, y=y2),
        )
        self._repository.add(line)
        self._logger.debug(
            "line_created",
            shape_id=str(line.id),
            start_x=x1,
            start_y=y1,
            end_x=x2,
            end_y=y2,
        )
        return line

    def create_circle(self, x: float, y: float, radius: float) -> Circle:
        """
        Create and store a new circle.

        Args:
            x: Center X-coordinate
            y: Center Y-coordinate
            radius: Circle radius (must be positive)

        Returns:
            The created circle
        """
        circle = Circle(
            center=Coordinates(x=x, y=y),
            radius=radius,
        )
        self._repository.add(circle)
        self._logger.debug(
            "circle_created",
            shape_id=str(circle.id),
            center_x=x,
            center_y=y,
            radius=radius,
        )
        return circle

    def create_square(self, x: float, y: float, side_length: float) -> Square:
        """
        Create and store a new square.

        Args:
            x: Top-left X-coordinate
            y: Top-left Y-coordinate
            side_length: Length of each side (must be positive)

        Returns:
            The created square
        """
        square = Square(
            top_left=Coordinates(x=x, y=y),
            side_length=side_length,
        )
        self._repository.add(square)
        self._logger.debug(
            "square_created",
            shape_id=str(square.id),
            top_left_x=x,
            top_left_y=y,
            side_length=side_length,
        )
        return square

    def delete_shape(self, shape_id: UUID) -> bool:
        """
        Delete a shape by its ID.

        Args:
            shape_id: ID of the shape to delete

        Returns:
            True if shape was deleted, False if not found
        """
        shape = self._repository.get(shape_id)
        if shape is None:
            self._logger.warning(
                "shape_not_found_for_deletion",
                shape_id=str(shape_id),
            )
            return False

        self._repository.remove(shape_id)
        self._logger.debug(
            "shape_deleted",
            shape_id=str(shape_id),
            shape_type=type(shape).__name__,
        )
        return True

    def get_all_shapes(self) -> list[IShape]:
        """
        Get all shapes.

        Returns:
            List of all shapes
        """
        shapes = self._repository.get_all()
        self._logger.debug(
            "shapes_retrieved",
            count=len(shapes),
        )
        return shapes

    def clear_all(self) -> None:
        """Delete all shapes."""
        count = self._repository.count()
        self._repository.clear()
        self._logger.debug(
            "all_shapes_cleared",
            deleted_count=count,
        )

    def count_shapes(self) -> int:
        """Get the total number of shapes."""
        return self._repository.count()
