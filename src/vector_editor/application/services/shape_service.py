"""
Application service for shape management.
"""

from pathlib import Path
from typing import Any
from uuid import UUID

import orjson
from src.vector_editor.config import AppConfig
from src.vector_editor.domain import PlacedShape
from src.vector_editor.domain.definitions import (
    CircleDefinition,
    EllipseDefinition,
    LineDefinition,
    PointDefinition,
    RectangleDefinition,
    SquareDefinition,
)
from src.vector_editor.domain.interfaces import IShapeRepository
from src.vector_editor.domain.primitives import Coordinates, Transform
from src.vector_editor.infrastructure.serialization import (
    dict_to_shape,
    shape_to_dict,
)
from src.vector_editor.logger import get_logger

logger = get_logger(__name__)


class ShapeService:
    """
    Application service coordinating shape operations.

    This service encapsulates the business logic for shape management
    and acts as a facade for the CLI layer.
    """

    def __init__(
        self, repository: IShapeRepository, config: AppConfig
    ) -> None:
        """
        Initialize the service with a repository.

        Args:
            repository: The shape repository to use
        """
        self._serialization_version = (
            config.file_system.db_json_serialization_version
        )
        self._repository = repository
        self._logger = logger.bind(component="ShapeService")

    def create_point(
        self, x: float, y: float, rotation: float = 0
    ) -> PlacedShape:
        """
        Create and store a new point.

        Args:
            x: X-coordinate
            y: Y-coordinate
            rotation: Rotation angle in degrees

        Returns:
            The created placed shape
        """
        definition = PointDefinition(coordinates=Coordinates(x=x, y=y))
        shape = PlacedShape(
            definition=definition,
            transform=Transform(rotation_deg=rotation),
        )
        self._repository.add(shape)
        self._logger.debug(
            "point_created",
            shape_id=str(shape.id),
            x=x,
            y=y,
            rotation=rotation,
        )
        return shape

    def create_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        rotation: float = 0,
    ) -> PlacedShape:
        """
        Create and store a new line segment from two points.

        Args:
            x1: Start point X-coordinate
            y1: Start point Y-coordinate
            x2: End point X-coordinate
            y2: End point Y-coordinate
            rotation: Rotation angle in degrees

        Returns:
            The created placed shape
        """
        definition = LineDefinition.from_points(
            start=Coordinates(x=x1, y=y1),
            end=Coordinates(x=x2, y=y2),
        )
        shape = PlacedShape(
            definition=definition,
            transform=Transform(rotation_deg=rotation),
        )
        self._repository.add(shape)
        self._logger.debug(
            "line_created",
            shape_id=str(shape.id),
            start_x=x1,
            start_y=y1,
            end_x=x2,
            end_y=y2,
            rotation=rotation,
        )
        return shape

    def create_line_polar(
        self,
        x: float,
        y: float,
        length: float,
        angle: float,
        rotation: float = 0,
    ) -> PlacedShape:
        """
        Create and store a new line segment from polar coordinates.

        Args:
            x: Origin X-coordinate
            y: Origin Y-coordinate
            length: Length of the line
            angle: Base angle in degrees
            rotation: Additional rotation angle in degrees

        Returns:
            The created placed shape
        """
        definition = LineDefinition.from_polar(
            origin=Coordinates(x=x, y=y),
            length=length,
            angle_deg=angle,
        )
        shape = PlacedShape(
            definition=definition,
            transform=Transform(rotation_deg=rotation),
        )
        self._repository.add(shape)
        self._logger.debug(
            "line_polar_created",
            shape_id=str(shape.id),
            origin_x=x,
            origin_y=y,
            length=length,
            base_angle=angle,
            rotation=rotation,
        )
        return shape

    def create_circle(
        self, x: float, y: float, radius: float, rotation: float = 0
    ) -> PlacedShape:
        """
        Create and store a new circle.

        Args:
            x: Center X-coordinate
            y: Center Y-coordinate
            radius: Circle radius (must be positive)
            rotation: Rotation angle in degrees

        Returns:
            The created placed shape
        """
        definition = CircleDefinition(
            center=Coordinates(x=x, y=y),
            radius=radius,
        )
        shape = PlacedShape(
            definition=definition,
            transform=Transform(rotation_deg=rotation),
        )
        self._repository.add(shape)
        self._logger.debug(
            "circle_created",
            shape_id=str(shape.id),
            center_x=x,
            center_y=y,
            radius=radius,
            rotation=rotation,
        )
        return shape

    def create_square(
        self, x: float, y: float, side_length: float, rotation: float = 0
    ) -> PlacedShape:
        """
        Create and store a new square.

        Args:
            x: Center X-coordinate
            y: Center Y-coordinate
            side_length: Length of each side (must be positive)
            rotation: Rotation angle in degrees

        Returns:
            The created placed shape
        """
        definition = SquareDefinition(
            center=Coordinates(x=x, y=y),
            side_length=side_length,
        )
        shape = PlacedShape(
            definition=definition,
            transform=Transform(rotation_deg=rotation),
        )
        self._repository.add(shape)
        self._logger.debug(
            "square_created",
            shape_id=str(shape.id),
            center_x=x,
            center_y=y,
            side_length=side_length,
            rotation=rotation,
        )
        return shape

    def create_rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        rotation: float = 0,
    ) -> PlacedShape:
        """
        Create and store a new rectangle.

        Args:
            x: Center X-coordinate
            y: Center Y-coordinate
            width: Width of the rectangle (must be positive)
            height: Height of the rectangle (must be positive)
            rotation: Rotation angle in degrees

        Returns:
            The created placed shape
        """
        definition = RectangleDefinition(
            center=Coordinates(x=x, y=y),
            width=width,
            height=height,
        )
        shape = PlacedShape(
            definition=definition,
            transform=Transform(rotation_deg=rotation),
        )
        self._repository.add(shape)
        self._logger.debug(
            "rectangle_created",
            shape_id=str(shape.id),
            center_x=x,
            center_y=y,
            width=width,
            height=height,
            rotation=rotation,
        )
        return shape

    def create_ellipse(
        self,
        x: float,
        y: float,
        radius_x: float,
        radius_y: float,
        rotation: float = 0,
    ) -> PlacedShape:
        """
        Create and store a new ellipse.

        Args:
            x: Center X-coordinate
            y: Center Y-coordinate
            radius_x: Horizontal radius (must be positive)
            radius_y: Vertical radius (must be positive)
            rotation: Rotation angle in degrees

        Returns:
            The created placed shape
        """
        definition = EllipseDefinition(
            center=Coordinates(x=x, y=y),
            radius_x=radius_x,
            radius_y=radius_y,
        )
        shape = PlacedShape(
            definition=definition,
            transform=Transform(rotation_deg=rotation),
        )
        self._repository.add(shape)
        self._logger.debug(
            "ellipse_created",
            shape_id=str(shape.id),
            center_x=x,
            center_y=y,
            radius_x=radius_x,
            radius_y=radius_y,
            rotation=rotation,
        )
        return shape

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
            shape_type=type(shape.definition).__name__,
        )
        return True

    def get_all_shapes(self) -> list[PlacedShape]:
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

    def save_to_file(self, path: Path) -> int:
        """
        Save all shapes to a JSON file.

        Args:
            path: File path to save to.

        Returns:
            Number of shapes saved.

        Raises:
            IOError: If file cannot be written.
        """

        shapes = self._repository.get_all()
        data: dict[str, Any] = {
            "version": self._serialization_version,
            "shapes": [shape_to_dict(s) for s in shapes],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))

        self._logger.debug(
            "shapes_saved_to_file",
            path=str(path),
            count=len(shapes),
        )
        return len(shapes)

    def load_from_file(self, path: Path) -> list[PlacedShape]:
        """
        Load shapes from a JSON file.

        Args:
            path: File path to load from.

        Returns:
            List of loaded shapes.

        Raises:
            FileNotFoundError: If file does not exist.
            ValueError: If file contains invalid data.
        """
        try:
            with open(path, "rb") as f:
                data = orjson.loads(f.read())
        except orjson.JSONDecodeError as e:
            self._logger.error(
                "invalid_json",
                error=str(e),
            )
            raise ValueError("JSONDecodeError") from e

        version = data.get("version", "1.0")
        if version != self._serialization_version:
            self._logger.warning(
                "loading_different_version",
                expected=self._serialization_version,
                got=version,
            )

        shapes_data = data.get("shapes", [])
        loaded: list[PlacedShape] = []
        errors: int = 0
        for item in shapes_data:
            try:
                shape = dict_to_shape(item)
                loaded.append(shape)
            except ValueError as e:
                errors += 1
                self._logger.error(
                    "skipping_invalid_shape",
                    error=str(e),
                )

        if errors:
            self._logger.warning(
                "shapes_loaded_with_errors",
                total_loaded=len(loaded),
                errors=errors,
            )
        else:
            self._logger.debug("shapes_loaded", count=len(loaded))

        return loaded

    def add_shapes(
        self, shapes: list[PlacedShape], skip_duplicates: bool = True
    ) -> int:
        """
        Add multiple shapes to the repository.

        Args:
            shapes: List of shapes to add.
            skip_duplicates: If True, skip shapes with IDs that already exist.

        Returns:
            Number of shapes actually added.

        Raises:
            ValueError: If skip_duplicates is False and a duplicate is found.
        """
        added = 0
        for shape in shapes:
            try:
                self._repository.add(shape)
                added += 1
            except ValueError as e:
                if "already exists" in str(e) and skip_duplicates:
                    self._logger.debug(
                        "skipping_duplicate_shape",
                        shape_id=str(shape.id),
                    )
                else:
                    raise
        self._logger.debug(
            "shapes_added",
            attempted=len(shapes),
            added=added,
        )
        return added
