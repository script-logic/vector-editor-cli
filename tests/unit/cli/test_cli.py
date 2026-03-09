"""
Unit tests for CLI interface.
"""

from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest
from click.testing import CliRunner, Result
from src.vector_editor.application.services import ShapeService
from src.vector_editor.cli import cli
from src.vector_editor.domain import PlacedShape
from src.vector_editor.domain.definitions import (
    CircleDefinition,
    EllipseDefinition,
    IShapeDefinition,
    LineDefinition,
    PointDefinition,
    RectangleDefinition,
    SquareDefinition,
)
from src.vector_editor.domain.primitives import Coordinates, Transform


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


def _create_mock_shape(definition: IShapeDefinition, rotation: float = 0.0):
    """Helper to create a mock PlacedShape."""
    shape = Mock(spec=PlacedShape)
    shape.id = uuid4()
    shape.transform = Transform(rotation_deg=rotation)
    shape.definition = definition
    shape.render.return_value = None
    return shape


def test_create_point(runner: CliRunner, mock_service: Mock) -> None:
    """Test point creation command."""
    expected_shape = _create_mock_shape(
        PointDefinition(coordinates=Coordinates(x=-1.5, y=2.5))
    )
    mock_service.create_point.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["point", "-1.5", "2.5"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_point.assert_called_once_with(-1.5, 2.5, rotation=0.0)


def test_create_point_with_angle(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test point creation with angle option."""
    expected_shape = _create_mock_shape(
        PointDefinition(coordinates=Coordinates(x=-1.5, y=2.5)), rotation=45.0
    )
    mock_service.create_point.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["point", "-1.5", "2.5", "--angle", "45"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_point.assert_called_once_with(-1.5, 2.5, rotation=45.0)


def test_create_line(runner: CliRunner, mock_service: Mock) -> None:
    """Test line creation command."""
    expected_shape = _create_mock_shape(
        LineDefinition.from_points(
            start=Coordinates(x=1.0, y=2.0),
            end=Coordinates(x=3.0, y=4.0),
        )
    )
    mock_service.create_line.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["line", "1", "2", "3", "4"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_line.assert_called_once_with(
        1.0, 2.0, 3.0, 4.0, rotation=0.0
    )


def test_create_line_with_angle(runner: CliRunner, mock_service: Mock) -> None:
    """Test line creation with angle option."""
    expected_shape = _create_mock_shape(
        LineDefinition.from_points(
            start=Coordinates(x=1.0, y=2.0),
            end=Coordinates(x=3.0, y=4.0),
        ),
        rotation=90.0,
    )
    mock_service.create_line.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["line", "1", "2", "3", "4", "--angle", "90"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_line.assert_called_once_with(
        1.0, 2.0, 3.0, 4.0, rotation=90.0
    )


def test_create_line_polar(runner: CliRunner, mock_service: Mock) -> None:
    """Test polar line creation command."""
    expected_shape = _create_mock_shape(
        LineDefinition.from_polar(
            origin=Coordinates(x=0.0, y=0.0),
            length=5.0,
            angle_deg=30.0,
        )
    )
    mock_service.create_line_polar.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["line-polar", "0", "0", "5", "30"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_line_polar.assert_called_once_with(
        0.0, 0.0, 5.0, 30.0, rotation=0.0
    )


def test_create_line_polar_with_angle(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test polar line creation with angle option."""
    expected_shape = _create_mock_shape(
        LineDefinition.from_polar(
            origin=Coordinates(x=0.0, y=0.0),
            length=5.0,
            angle_deg=30.0,
        ),
        rotation=15.0,
    )
    mock_service.create_line_polar.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["line-polar", "0", "0", "5", "30", "--angle", "15"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_line_polar.assert_called_once_with(
        0.0, 0.0, 5.0, 30.0, rotation=15.0
    )


def test_create_circle(runner: CliRunner, mock_service: Mock) -> None:
    """Test circle creation command."""
    expected_shape = _create_mock_shape(
        CircleDefinition(center=Coordinates(x=0.0, y=0.0), radius=5.0)
    )
    mock_service.create_circle.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["circle", "0", "0", "5"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_circle.assert_called_once_with(
        0.0, 0.0, 5.0, rotation=0.0
    )


def test_create_circle_with_invalid_radius(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test circle creation with negative radius."""
    mock_service.create_circle.side_effect = ValueError(
        "Radius must be positive"
    )

    result: Result = runner.invoke(
        cli,
        ["circle", "0", "0", "--", "-5"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code != 0
    assert "Error: Radius must be positive" in result.output


def test_create_square(runner: CliRunner, mock_service: Mock) -> None:
    """Test square creation command."""
    expected_shape = _create_mock_shape(
        SquareDefinition(center=Coordinates(x=1.0, y=2.0), side_length=3.0)
    )
    mock_service.create_square.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["square", "1", "2", "3"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_square.assert_called_once_with(
        1.0, 2.0, 3.0, rotation=0.0
    )


def test_create_rectangle(runner: CliRunner, mock_service: Mock) -> None:
    """Test rectangle creation command."""
    expected_shape = _create_mock_shape(
        RectangleDefinition(
            center=Coordinates(x=2.0, y=3.0), width=4.0, height=5.0
        )
    )
    mock_service.create_rectangle.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["rectangle", "2", "3", "4", "5"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_rectangle.assert_called_once_with(
        2.0, 3.0, 4.0, 5.0, rotation=0.0
    )


def test_create_ellipse(runner: CliRunner, mock_service: Mock) -> None:
    """Test ellipse creation command."""
    expected_shape = _create_mock_shape(
        EllipseDefinition(
            center=Coordinates(x=3.0, y=4.0), radius_x=2.0, radius_y=3.0
        )
    )
    mock_service.create_ellipse.return_value = expected_shape

    result: Result = runner.invoke(
        cli,
        ["ellipse", "3", "4", "2", "3"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Created" in result.output
    mock_service.create_ellipse.assert_called_once_with(
        3.0, 4.0, 2.0, 3.0, rotation=0.0
    )


def test_list_shapes_empty(runner: CliRunner, mock_service: Mock) -> None:
    """Test listing shapes when none exist."""
    mock_service.get_all_shapes.return_value = []

    result: Result = runner.invoke(
        cli,
        ["list"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "📭 No shapes created yet." in result.output


def test_list_shapes_with_data(runner: CliRunner, mock_service: Mock) -> None:
    """Test listing shapes with existing data."""
    shapes: list[PlacedShape] = [
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
    mock_service.get_all_shapes.return_value = shapes

    result: Result = runner.invoke(
        cli,
        ["list"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "📋 Shapes (2 total):" in result.output
    assert "Point" in result.output
    assert "Circle" in result.output


def test_delete_shape_with_full_uuid(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test deleting shape with full UUID."""
    shape_id: UUID = uuid4()
    mock_service.delete_shape.return_value = True

    result: Result = runner.invoke(
        cli,
        ["delete", str(shape_id)],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert f"✔ Deleted shape {shape_id}" in result.output
    mock_service.delete_shape.assert_called_once_with(shape_id)


def test_delete_shape_with_short_id(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test deleting shape with short ID (first 8 chars)."""
    shape = PlacedShape(
        definition=PointDefinition(coordinates=Coordinates(x=1.0, y=2.0)),
        transform=Transform(rotation_deg=0),
    )
    short_id: str = str(shape.id)[:8]

    mock_service.get_all_shapes.return_value = [shape]
    mock_service.delete_shape.return_value = True

    result: Result = runner.invoke(
        cli,
        ["delete", short_id],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert f"✔ Deleted shape {short_id}" in result.output
    mock_service.delete_shape.assert_called_once_with(shape.id)


def test_delete_shape_with_ambiguous_short_id(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test deleting shape with ambiguous short ID."""
    id1 = UUID("12345678-1234-1234-1234-123456789abc")
    id2 = UUID("12345678-1234-1234-1234-123456789def")
    short_id = "12345678"

    shape1 = PlacedShape(
        definition=PointDefinition(coordinates=Coordinates(x=1.0, y=2.0)),
        transform=Transform(rotation_deg=0),
        id=id1,
    )
    shape2 = PlacedShape(
        definition=PointDefinition(coordinates=Coordinates(x=3.0, y=4.0)),
        transform=Transform(rotation_deg=0),
        id=id2,
    )

    mock_service.get_all_shapes.return_value = [shape1, shape2]

    result: Result = runner.invoke(
        cli,
        ["delete", short_id],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code != 0
    assert "Multiple shapes match ID" in result.output
    mock_service.delete_shape.assert_not_called()


def test_delete_shape_not_found(runner: CliRunner, mock_service: Mock) -> None:
    """Test deleting non-existent shape."""
    shape_id: UUID = uuid4()
    mock_service.delete_shape.return_value = False

    result: Result = runner.invoke(
        cli,
        ["delete", str(shape_id)],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code != 0
    assert f"Error: Shape with ID {shape_id} not found" in result.output


def test_count_shapes(runner: CliRunner, mock_service: Mock) -> None:
    """Test counting shapes."""
    mock_service.count_shapes.return_value = 5

    result: Result = runner.invoke(
        cli,
        ["count"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "📊 Total shapes: 5" in result.output


def test_clear_all_with_confirmation(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test clearing all shapes with confirmation."""
    mock_service.count_shapes.return_value = 3

    result: Result = runner.invoke(
        cli,
        ["clear"],
        input="y\n",
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Deleted all 3 shapes" in result.output
    mock_service.clear_all.assert_called_once()


def test_clear_all_without_confirmation(
    runner: CliRunner, mock_service: Mock
) -> None:
    """Test clearing all shapes without confirmation."""
    mock_service.count_shapes.return_value = 3

    result: Result = runner.invoke(
        cli,
        ["clear", "--yes"],
        obj={"shape_service": mock_service},
    )

    assert result.exit_code == 0
    assert "✔ Deleted all 3 shapes" in result.output
    mock_service.clear_all.assert_called_once()


def test_help_command(runner: CliRunner) -> None:
    """Test help command."""
    result: Result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Vector Editor CLI" in result.output
    assert "Commands:" in result.output
    assert "line-polar" in result.output
    assert "rectangle" in result.output
    assert "ellipse" in result.output
