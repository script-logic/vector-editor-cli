"""
CLI application for vector editor.
"""

from uuid import UUID

import click
from src.vector_editor.application.services import ShapeService
from src.vector_editor.logger import get_logger

from .formatting import format_shape, format_shape_list

logger = get_logger(__name__)


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Vector Editor CLI - Create and manage geometric shapes.

    This tool allows you to create points, lines, circles, and squares,
    list them, and delete them.
    """
    ctx.ensure_object(dict)
    if not ctx.obj:
        raise click.ClickException("Context object must be a non empty dict.")
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


def _get_shape_service(ctx: click.Context) -> ShapeService:
    """Get ShapeService from context."""
    shape_service = ctx.obj.get("shape_service")
    if shape_service is None:
        raise click.ClickException(
            "Shape service not initialized. This is a bug."
        )
    return shape_service


def _parse_float(value: str, coord_name: str) -> float:
    """
    Parse a string into float with error handling.

    Args:
        value: String to parse
        coord_name: Name of the coordinate for error message

    Returns:
        Float value

    Raises:
        click.ClickException: If value cannot be converted to float
    """
    try:
        return float(value)
    except ValueError:
        raise click.ClickException(
            f"Invalid number for {coord_name}: '{value}'. Expected a number."
        )


@cli.command(
    "point",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
)
@click.argument("x", required=False)
@click.argument("y", required=False)
@click.pass_context
def create_point(ctx: click.Context, x: str | None, y: str | None) -> None:
    """
    Create a new point at coordinates <x> <y>.
    """
    service = _get_shape_service(ctx)

    args = ctx.args

    all_coords = [coord for coord in [x, y] if coord is not None]
    all_coords.extend(args)

    if len(all_coords) != 2:
        raise click.ClickException(
            f"Expected 2 coordinates, got {len(all_coords)}"
            "\nUsage: point <x> <y> (e.g., 'point 10 20' or 'point -5.5 3')"
        )

    try:
        x_val = _parse_float(all_coords[0], "<x>")
        y_val = _parse_float(all_coords[1], "<y>")
        point = service.create_point(x_val, y_val)
        click.echo(f"✅ Created: {format_shape(point)}")
        logger.debug("point_created_via_cli", x=x_val, y=y_val)
    except ValueError as e:
        logger.debug("point_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "line",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
)
@click.argument("x1", required=False)
@click.argument("y1", required=False)
@click.argument("x2", required=False)
@click.argument("y2", required=False)
@click.pass_context
def create_line(
    ctx: click.Context,
    x1: str | None,
    y1: str | None,
    x2: str | None,
    y2: str | None,
) -> None:
    """
    Create a new line from (<start_x>, <start_y>) to (<end_x>, <end_y>).
    """
    service = _get_shape_service(ctx)

    args = ctx.args
    all_coords = [coord for coord in [x1, y1, x2, y2] if coord is not None]
    all_coords.extend(args)

    if len(all_coords) != 4:
        raise click.ClickException(
            f"Expected 4 coordinates, got {len(all_coords)}"
            "\nUsage: line <start_x> <start_y> <end_x> <end_y> "
            "(e.g., 'line 10.3 20 -30 40')"
        )

    try:
        x1_val = _parse_float(all_coords[0], "<start_x>")
        y1_val = _parse_float(all_coords[1], "<start_y>")
        x2_val = _parse_float(all_coords[2], "<end_x>")
        y2_val = _parse_float(all_coords[3], "<end_y>")
        line = service.create_line(x1_val, y1_val, x2_val, y2_val)
        click.echo(f"✅ Created: {format_shape(line)}")
        logger.debug(
            "line_created_via_cli", x1=x1_val, y1=y1_val, x2=x2_val, y2=y2_val
        )
    except ValueError as e:
        logger.debug("line_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "circle",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
)
@click.argument("x", required=False)
@click.argument("y", required=False)
@click.argument("radius", required=False)
@click.pass_context
def create_circle(
    ctx: click.Context,
    x: str | None,
    y: str | None,
    radius: str | None,
) -> None:
    """
    Create a new circle with center at (<center_x>, <center_y>)
    and given <radius>.
    """
    service = _get_shape_service(ctx)

    args = ctx.args
    all_args = [arg for arg in [x, y, radius] if arg is not None]
    all_args.extend(args)

    if len(all_args) != 3:
        raise click.ClickException(
            f"Expected 3 arguments, got {len(all_args)}: {' '.join(all_args)}. "
            "Usage: circle <center_x> <center_y> <radius> "
            "(e.g., 'circle 10 20 5')"
        )

    try:
        x_val = _parse_float(all_args[0], "<x>")
        y_val = _parse_float(all_args[1], "<y>")
        radius_val = _parse_float(all_args[2], "<radius>")

        if radius_val <= 0:
            raise click.ClickException(
                f"Radius must be positive, got {radius_val}"
            )

        circle = service.create_circle(x_val, y_val, radius_val)
        click.echo(f"✅ Created: {format_shape(circle)}")
        logger.debug(
            "circle_created_via_cli", x=x_val, y=y_val, radius=radius_val
        )
    except ValueError as e:
        logger.debug("circle_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "square",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
)
@click.argument("x", required=False)
@click.argument("y", required=False)
@click.argument("side_length", required=False)
@click.pass_context
def create_square(
    ctx: click.Context,
    x: str | None,
    y: str | None,
    side_length: str | None,
) -> None:
    """
    Create a new square with top-left corner at (<top_left_x>, <top_left_y>)
    and given <side_length>.
    """
    service = _get_shape_service(ctx)

    args = ctx.args
    all_args = [arg for arg in [x, y, side_length] if arg is not None]
    all_args.extend(args)

    if len(all_args) != 3:
        raise click.ClickException(
            f"Expected 3 arguments, got {len(all_args)}: {' '.join(all_args)}. "
            "Usage: square <top_left_x> <top_left_y> <side_length> "
            "(e.g., 'square 10 20 5')"
        )

    try:
        x_val = _parse_float(all_args[0], "<top_left_x>")
        y_val = _parse_float(all_args[1], "<top_left_y>")
        side_val = _parse_float(all_args[2], "<side_length>")

        if side_val <= 0:
            raise click.ClickException(
                f"Side length must be positive, got {side_val}"
            )

        square = service.create_square(x_val, y_val, side_val)
        click.echo(f"✅ Created: {format_shape(square)}")
        logger.debug(
            "square_created_via_cli", x=x_val, y=y_val, side_length=side_val
        )
    except ValueError as e:
        logger.debug("square_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command("list")
@click.pass_context
def list_shapes(ctx: click.Context) -> None:
    """List all created shapes."""
    service = _get_shape_service(ctx)
    shapes = service.get_all_shapes()
    click.echo(format_shape_list(shapes))
    logger.debug("shapes_listed_via_cli", count=len(shapes))


@cli.command("delete")
@click.argument("shape_id", type=str)
@click.pass_context
def delete_shape(ctx: click.Context, shape_id: str) -> None:
    """Delete a shape by its ID (first 8 characters are enough)."""
    service = _get_shape_service(ctx)
    try:
        full_uuid: UUID | None = None

        try:
            full_uuid = UUID(shape_id)
        except ValueError:
            all_shapes = service.get_all_shapes()
            matching = [
                s for s in all_shapes if str(s.id).startswith(shape_id)
            ]

            if not matching:
                raise click.ClickException(
                    f"No shape found with ID starting with '{shape_id}'"
                )

            if len(matching) > 1:
                shapes_str = "\n".join(
                    f"  {format_shape(s)}" for s in matching
                )
                raise click.ClickException(
                    f"Multiple shapes match ID '{shape_id}':\n{shapes_str}\n"
                    "Please use full ID."
                )

            full_uuid = matching[0].id

        if full_uuid and service.delete_shape(full_uuid):
            click.echo(f"✅ Deleted shape {shape_id}")
            logger.debug("shape_deleted_via_cli", shape_id=str(full_uuid))
        else:
            raise click.ClickException(f"Shape with ID {shape_id} not found")

    except (ValueError, KeyError) as e:
        logger.error("shape_deletion_failed", shape_id=shape_id, error=str(e))
        raise click.ClickException(str(e))


@cli.command("clear")
@click.confirmation_option(
    prompt="Are you sure you want to delete ALL shapes?"
)
@click.pass_context
def clear_all(ctx: click.Context) -> None:
    """Delete all shapes."""
    service = _get_shape_service(ctx)
    count = service.count_shapes()
    service.clear_all()
    click.echo(f"✅ Deleted all {count} shapes")
    logger.debug("all_shapes_cleared_via_cli", count=count)


@cli.command("count")
@click.pass_context
def count_shapes(ctx: click.Context) -> None:
    """Show total number of shapes."""
    service = _get_shape_service(ctx)
    count = service.count_shapes()
    click.echo(f"📊 Total shapes: {count}")
    logger.debug("count_shapes_via_cli", count=count)


@cli.command("help")
@click.argument("command", required=False)
@click.pass_context
def help_command(ctx: click.Context, command: str | None) -> None:
    """Show help for a command."""
    if command:
        cmd = cli.get_command(ctx, command)
        if cmd:
            click.echo(cmd.get_help(ctx))
        else:
            click.echo(f"Unknown command: {command}")
    else:
        click.echo(ctx.get_help())
