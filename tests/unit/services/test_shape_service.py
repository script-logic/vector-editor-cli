"""
Unit tests for ShapeService.
"""

from unittest.mock import Mock, create_autospec
from uuid import uuid4

import pytest
from src.vector_editor.application.services import ShapeService
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


@pytest.fixture
def mock_repository() -> Mock:
    """Fixture for mocked repository."""
    return create_autospec(IShapeRepository)


@pytest.fixture
def mock_config() -> Mock:
    return Mock()


@pytest.fixture
def shape_service(mock_repository: Mock, mock_config: Mock) -> ShapeService:
    """Fixture for ShapeService with mocked repository."""
    return ShapeService(repository=mock_repository, config=mock_config)


def test_create_point(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a point."""
    x, y = -1.5, 2.5
    rotation = 45.0

    shape = shape_service.create_point(x, y, rotation=rotation)

    assert isinstance(shape, PlacedShape)
    assert isinstance(shape.definition, PointDefinition)
    assert shape.definition.coordinates.x == x
    assert shape.definition.coordinates.y == y
    assert shape.transform.rotation_deg == rotation

    mock_repository.add.assert_called_once_with(shape)


def test_create_point_default_rotation(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a point with default rotation."""
    x, y = 10.0, 20.0

    shape = shape_service.create_point(x, y)

    assert shape.transform.rotation_deg == 0
    mock_repository.add.assert_called_once_with(shape)


def test_create_line(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a line from two points."""
    x1, y1, x2, y2 = 1.0, 2.0, -3.0, 4.0
    rotation = 90.0

    shape = shape_service.create_line(x1, y1, x2, y2, rotation=rotation)

    assert isinstance(shape, PlacedShape)
    assert isinstance(shape.definition, LineDefinition)
    assert shape.definition.start is not None
    assert shape.definition.start is not None
    assert shape.definition.end is not None
    assert shape.definition.end is not None
    assert shape.definition.start.x == x1
    assert shape.definition.start.y == y1
    assert shape.definition.end.x == x2
    assert shape.definition.end.y == y2
    assert shape.definition.representation.value == "two_points"
    assert shape.transform.rotation_deg == rotation

    mock_repository.add.assert_called_once_with(shape)


def test_create_line_polar(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a line from polar coordinates."""
    x, y, length, angle = 5.0, 5.0, 10.0, 30.0
    rotation = 15.0

    shape = shape_service.create_line_polar(
        x, y, length, angle, rotation=rotation
    )

    assert isinstance(shape, PlacedShape)
    assert isinstance(shape.definition, LineDefinition)
    assert shape.definition.origin is not None
    assert shape.definition.origin is not None
    assert shape.definition.origin.x == x
    assert shape.definition.origin.y == y
    assert shape.definition.length == length
    assert shape.definition.angle_deg == angle % 360
    assert shape.definition.representation.value == "polar"
    assert shape.transform.rotation_deg == rotation

    mock_repository.add.assert_called_once_with(shape)


def test_create_circle(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a circle."""
    x, y, radius = 0.0, 0.0, 5.0
    rotation = 30.0

    shape = shape_service.create_circle(x, y, radius, rotation=rotation)

    assert isinstance(shape, PlacedShape)
    assert isinstance(shape.definition, CircleDefinition)
    assert shape.definition.center.x == x
    assert shape.definition.center.y == y
    assert shape.definition.radius == radius
    assert shape.transform.rotation_deg == rotation

    mock_repository.add.assert_called_once_with(shape)


def test_create_circle_with_negative_radius_raises_error(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a circle with negative radius raises error."""
    with pytest.raises(ValueError, match="Radius must be positive"):
        shape_service.create_circle(x=0.0, y=0.0, radius=-5.0)

    mock_repository.add.assert_not_called()


def test_create_square(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a square."""
    x, y, side = 1.0, 2.0, 3.0
    rotation = 60.0

    shape = shape_service.create_square(x, y, side, rotation=rotation)

    assert isinstance(shape, PlacedShape)
    assert isinstance(shape.definition, SquareDefinition)
    assert shape.definition.center.x == x
    assert shape.definition.center.y == y
    assert shape.definition.side_length == side
    assert shape.transform.rotation_deg == rotation

    mock_repository.add.assert_called_once_with(shape)


def test_create_square_with_negative_side_raises_error(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a square with negative side length raises error."""
    with pytest.raises(ValueError, match="Side length must be positive"):
        shape_service.create_square(x=1.0, y=2.0, side_length=-3.0)

    mock_repository.add.assert_not_called()


def test_create_rectangle(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a rectangle."""
    x, y, width, height = 2.0, 3.0, 4.0, 5.0
    rotation = 120.0

    shape = shape_service.create_rectangle(
        x, y, width, height, rotation=rotation
    )

    assert isinstance(shape, PlacedShape)
    assert isinstance(shape.definition, RectangleDefinition)
    assert shape.definition.center.x == x
    assert shape.definition.center.y == y
    assert shape.definition.width == width
    assert shape.definition.height == height
    assert shape.transform.rotation_deg == rotation

    mock_repository.add.assert_called_once_with(shape)


def test_create_rectangle_with_negative_dimensions_raises_error(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a rectangle with negative dimensions raises error."""
    with pytest.raises(ValueError, match="Width must be positive"):
        shape_service.create_rectangle(x=0.0, y=0.0, width=-2.0, height=3.0)
    with pytest.raises(ValueError, match="Height must be positive"):
        shape_service.create_rectangle(x=0.0, y=0.0, width=2.0, height=-3.0)

    mock_repository.add.assert_not_called()


def test_create_ellipse(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating an ellipse."""
    x, y, rx, ry = 3.0, 4.0, 2.0, 3.0
    rotation = 45.0

    shape = shape_service.create_ellipse(x, y, rx, ry, rotation=rotation)

    assert isinstance(shape, PlacedShape)
    assert isinstance(shape.definition, EllipseDefinition)
    assert shape.definition.center.x == x
    assert shape.definition.center.y == y
    assert shape.definition.radius_x == rx
    assert shape.definition.radius_y == ry
    assert shape.transform.rotation_deg == rotation

    mock_repository.add.assert_called_once_with(shape)


def test_create_ellipse_with_negative_radii_raises_error(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating an ellipse with negative radii raises error."""
    with pytest.raises(ValueError, match="X-radius must be positive"):
        shape_service.create_ellipse(x=0.0, y=0.0, radius_x=-1.0, radius_y=2.0)
    with pytest.raises(ValueError, match="Y-radius must be positive"):
        shape_service.create_ellipse(x=0.0, y=0.0, radius_x=1.0, radius_y=-2.0)

    mock_repository.add.assert_not_called()


def test_delete_shape_success(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test successful shape deletion."""
    shape_id = uuid4()
    definition = PointDefinition(coordinates=Coordinates(x=1.0, y=2.0))
    shape = PlacedShape(definition=definition, id=shape_id)
    mock_repository.get.return_value = shape

    result = shape_service.delete_shape(shape_id)

    assert result is True
    mock_repository.get.assert_called_once_with(shape_id)
    mock_repository.remove.assert_called_once_with(shape_id)


def test_delete_shape_not_found(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test deleting non-existent shape."""
    shape_id = uuid4()
    mock_repository.get.return_value = None

    result = shape_service.delete_shape(shape_id)

    assert result is False
    mock_repository.get.assert_called_once_with(shape_id)
    mock_repository.remove.assert_not_called()


def test_get_all_shapes(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test getting all shapes."""
    expected_shapes: list[PlacedShape] = [
        PlacedShape(
            definition=PointDefinition(coordinates=Coordinates(x=1.0, y=2.0)),
            transform=Transform(rotation_deg=0),
        ),
        PlacedShape(
            definition=CircleDefinition(
                center=Coordinates(x=0.0, y=0.0), radius=5.0
            ),
            transform=Transform(rotation_deg=90),
        ),
    ]
    mock_repository.get_all.return_value = expected_shapes

    shapes = shape_service.get_all_shapes()

    assert shapes == expected_shapes
    assert len(shapes) == 2
    mock_repository.get_all.assert_called_once()


def test_clear_all(shape_service: ShapeService, mock_repository: Mock) -> None:
    """Test clearing all shapes."""
    mock_repository.count.return_value = 3

    shape_service.clear_all()

    mock_repository.count.assert_called_once()
    mock_repository.clear.assert_called_once()


def test_count_shapes(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test counting shapes."""
    mock_repository.count.return_value = 5

    count = shape_service.count_shapes()

    assert count == 5
    mock_repository.count.assert_called_once()
