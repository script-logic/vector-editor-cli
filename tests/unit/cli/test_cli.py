"""
Unit tests for CLI interface.
"""

from unittest.mock import Mock, patch
from uuid import UUID, uuid4

import pytest
from click.testing import CliRunner, Result
from src.vector_editor.application.services.shape_service import ShapeService
from src.vector_editor.cli.app import cli
from src.vector_editor.domain.entities import (
    Circle,
    Coordinates,
    Line,
    Point,
    Square,
)


@pytest.fixture
def mock_service() -> Mock:
    """Fixture for mocked ShapeService."""
    mock = Mock(spec=ShapeService)
    mock._repository = Mock()
    return mock


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for Click CLI runner."""
    return CliRunner()


def test_create_point(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test point creation command."""
    expected_point = Point(coordinates=Coordinates(x=1.5, y=2.5))
    mock_service.create_point.return_value = expected_point

    result: Result = runner.invoke(
        cli,
        ["point", "1.5", "2.5"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "✅ Created" in result.output
    mock_service.create_point.assert_called_once_with(1.5, 2.5)


def test_create_line(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test line creation command."""
    expected_line = Line(
        start=Coordinates(x=1.0, y=2.0),
        end=Coordinates(x=3.0, y=4.0),
    )
    mock_service.create_line.return_value = expected_line

    result: Result = runner.invoke(
        cli,
        ["line", "1", "2", "3", "4"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "✅ Created" in result.output
    mock_service.create_line.assert_called_once_with(1.0, 2.0, 3.0, 4.0)


def test_create_circle(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test circle creation command."""
    expected_circle = Circle(
        center=Coordinates(x=0.0, y=0.0),
        radius=5.0,
    )
    mock_service.create_circle.return_value = expected_circle

    result: Result = runner.invoke(
        cli,
        ["circle", "0", "0", "5"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "✅ Created" in result.output
    mock_service.create_circle.assert_called_once_with(0.0, 0.0, 5.0)


def test_create_circle_with_invalid_radius(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test circle creation with negative radius."""
    mock_service.create_circle.side_effect = ValueError(
        "Radius must be positive"
    )

    result: Result = runner.invoke(
        cli,
        ["circle", "0", "0", "--", "-5"],
        obj={"service": mock_service},
    )

    assert result.exit_code != 0
    assert "Error: Radius must be positive" in result.output


def test_create_square(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test square creation command."""
    expected_square = Square(
        top_left=Coordinates(x=1.0, y=2.0),
        side_length=3.0,
    )
    mock_service.create_square.return_value = expected_square

    result: Result = runner.invoke(
        cli,
        ["square", "1", "2", "3"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "✅ Created" in result.output
    mock_service.create_square.assert_called_once_with(1.0, 2.0, 3.0)


def test_list_shapes_empty(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test listing shapes when none exist."""
    mock_service.get_all_shapes.return_value = []

    result: Result = runner.invoke(
        cli,
        ["list"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "📭 No shapes created yet." in result.output


def test_list_shapes_with_data(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test listing shapes with existing data."""
    shapes: list[Point | Circle] = [
        Point(coordinates=Coordinates(x=1.0, y=2.0)),
        Circle(center=Coordinates(x=0.0, y=0.0), radius=5.0),
    ]
    mock_service.get_all_shapes.return_value = shapes

    result: Result = runner.invoke(
        cli,
        ["list"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "📋 Shapes (2 total):" in result.output
    assert "Point" in result.output
    assert "Circle" in result.output


def test_delete_shape_with_full_uuid(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test deleting shape with full UUID."""
    shape_id: UUID = uuid4()
    mock_service.delete_shape.return_value = True

    result: Result = runner.invoke(
        cli,
        ["delete", str(shape_id)],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert f"✅ Deleted shape {shape_id}" in result.output
    mock_service.delete_shape.assert_called_once_with(shape_id)


def test_delete_shape_with_short_id(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test deleting shape with short ID (first 8 chars)."""
    point = Point(coordinates=Coordinates(x=1.0, y=2.0))
    short_id: str = str(point.id)[:8]

    mock_service.get_all_shapes.return_value = [point]
    mock_service.delete_shape.return_value = True

    result: Result = runner.invoke(
        cli,
        ["delete", short_id],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert f"✅ Deleted shape {short_id}" in result.output
    mock_service.delete_shape.assert_called_once_with(point.id)


def test_delete_shape_with_ambiguous_short_id(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test deleting shape with ambiguous short ID."""
    id1 = UUID("12345678-1234-1234-1234-123456789abc")
    id2 = UUID("12345678-1234-1234-1234-123456789def")
    short_id = "12345678"

    with patch("src.vector_editor.domain.entities.shape.uuid4") as mock_uuid:
        mock_uuid.side_effect = [id1, id2]
        point1 = Point(coordinates=Coordinates(x=1.0, y=2.0))
        point2 = Point(coordinates=Coordinates(x=3.0, y=4.0))

    mock_service.get_all_shapes.return_value = [point1, point2]
    mock_service.delete_shape.return_value = False

    result: Result = runner.invoke(
        cli,
        ["delete", short_id],
        obj={"service": mock_service},
    )

    assert result.exit_code != 0
    assert "Multiple shapes match ID" in result.output
    mock_service.delete_shape.assert_not_called()


def test_delete_shape_not_found(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test deleting non-existent shape."""
    shape_id: UUID = uuid4()
    mock_service.delete_shape.return_value = False

    result: Result = runner.invoke(
        cli,
        ["delete", str(shape_id)],
        obj={"service": mock_service},
    )

    assert result.exit_code != 0
    assert f"Error: Shape with ID {shape_id} not found" in result.output


def test_count_shapes(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test counting shapes."""
    mock_service.count_shapes.return_value = 5

    result: Result = runner.invoke(
        cli,
        ["count"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "📊 Total shapes: 5" in result.output


def test_clear_all_with_confirmation(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test clearing all shapes with confirmation."""
    mock_service.count_shapes.return_value = 3

    result: Result = runner.invoke(
        cli,
        ["clear"],
        input="y\n",
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "✅ Deleted all 3 shapes" in result.output
    mock_service.clear_all.assert_called_once()


def test_clear_all_without_confirmation(
    runner: CliRunner,
    mock_service: Mock,
) -> None:
    """Test clearing all shapes without confirmation."""
    mock_service.count_shapes.return_value = 3

    result: Result = runner.invoke(
        cli,
        ["clear", "--yes"],
        obj={"service": mock_service},
    )

    assert result.exit_code == 0
    assert "✅ Deleted all 3 shapes" in result.output
    mock_service.clear_all.assert_called_once()


def test_help_command(runner: CliRunner) -> None:
    """Test help command."""
    result: Result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Vector Editor CLI" in result.output
    assert "Commands:" in result.output
