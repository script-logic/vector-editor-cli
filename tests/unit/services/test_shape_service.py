"""
Unit tests for ShapeService.
"""

from unittest.mock import Mock, create_autospec
from uuid import uuid4

import pytest
from src.vector_editor.application.services.shape_service import ShapeService
from src.vector_editor.domain.entities import (
    Circle,
    Coordinates,
    Line,
    Point,
    Square,
)
from src.vector_editor.domain.interfaces import IShapeRepository

from vector_editor.domain.entities.shape import IShape


@pytest.fixture
def mock_repository() -> Mock:
    """Fixture for mocked repository."""
    return create_autospec(IShapeRepository)


@pytest.fixture
def shape_service(mock_repository: Mock) -> ShapeService:
    """Fixture for ShapeService with mocked repository."""
    return ShapeService(repository=mock_repository)


def test_create_point(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a point."""
    point = shape_service.create_point(x=-1.5, y=2.5)

    assert isinstance(point, Point)
    assert point.coordinates.x == -1.5
    assert point.coordinates.y == 2.5
    mock_repository.add.assert_called_once_with(point)


def test_create_line(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a line."""
    line = shape_service.create_line(x1=1.0, y1=2.0, x2=-3.0, y2=4.0)

    assert isinstance(line, Line)
    assert line.start.x == 1.0
    assert line.start.y == 2.0
    assert line.end.x == -3.0
    assert line.end.y == 4.0
    mock_repository.add.assert_called_once_with(line)


def test_create_circle(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a circle."""
    circle = shape_service.create_circle(x=0.0, y=0.0, radius=5.0)

    assert isinstance(circle, Circle)
    assert circle.center.x == 0.0
    assert circle.center.y == 0.0
    assert circle.radius == 5.0
    mock_repository.add.assert_called_once_with(circle)


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
    square = shape_service.create_square(x=1.0, y=2.0, side_length=3.0)

    assert isinstance(square, Square)
    assert square.top_left.x == 1.0
    assert square.top_left.y == 2.0
    assert square.side_length == 3.0
    mock_repository.add.assert_called_once_with(square)


def test_create_square_with_negative_side_raises_error(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test creating a square with negative side length raises error."""
    with pytest.raises(ValueError, match="Side length must be positive"):
        shape_service.create_square(x=1.0, y=2.0, side_length=-3.0)

    mock_repository.add.assert_not_called()


def test_delete_shape_success(
    shape_service: ShapeService, mock_repository: Mock
) -> None:
    """Test successful shape deletion."""
    shape_id = uuid4()
    mock_shape = Mock(spec=Point)
    mock_repository.get.return_value = mock_shape

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
    expected_shapes: list[IShape] = [
        Point(coordinates=Coordinates(x=1.0, y=2.0)),
        Circle(center=Coordinates(x=0.0, y=0.0), radius=5.0),
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
