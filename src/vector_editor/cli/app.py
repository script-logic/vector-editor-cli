"""
CLI application for vector editor.
"""

from uuid import UUID

import click
from src.vector_editor.application.services import ShapeService
from src.vector_editor.logger import get_logger

from .formatting import format_shape, format_shape_list

logger = get_logger(__name__)


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


def _parse_angle(ctx: click.Context, param: str, value: str | None) -> float:
    """Parse angle option, default to 0."""
    if value is None:
        return 0.0
    try:
        return float(value)
    except ValueError:
        raise click.ClickException(
            f"Invalid angle value: '{value}'. Expected a number."
        )


_angle_option = click.option(
    "--angle",
    "-a",
    type=str,
    callback=_parse_angle,
    help="Rotation angle in degrees (default: 0).",
)


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Vector Editor CLI - Create and manage geometric shapes.

    This tool allows you to create points, lines, circles, squares,
    rectangles, ellipses, list them, and delete them.
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


@cli.command(
    "point",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("x", type=str)
@click.argument("y", type=str)
@_angle_option
@click.pass_context
def create_point(ctx: click.Context, x: str, y: str, angle: float) -> None:
    """
    Create a new point at coordinates <x> <y>.
    """
    service = _get_shape_service(ctx)

    try:
        x_val = _parse_float(x, "<x>")
        y_val = _parse_float(y, "<y>")
        shape = service.create_point(x_val, y_val, rotation=angle)
        click.echo(f"✔ Created: {format_shape(shape)}")
        logger.debug(
            "point_created_via_cli",
            x=x_val,
            y=y_val,
            angle=angle,
        )
    except ValueError as e:
        logger.debug("point_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "line",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("x1", type=str)
@click.argument("y1", type=str)
@click.argument("x2", type=str)
@click.argument("y2", type=str)
@_angle_option
@click.pass_context
def create_line(
    ctx: click.Context,
    x1: str,
    y1: str,
    x2: str,
    y2: str,
    angle: float,
) -> None:
    """
    Create a new line from (<x1>, <y1>) to (<x2>, <y2>).
    """
    service = _get_shape_service(ctx)

    try:
        x1_val = _parse_float(x1, "<x1>")
        y1_val = _parse_float(y1, "<y1>")
        x2_val = _parse_float(x2, "<x2>")
        y2_val = _parse_float(y2, "<y2>")
        shape = service.create_line(
            x1_val, y1_val, x2_val, y2_val, rotation=angle
        )
        click.echo(f"✔ Created: {format_shape(shape)}")
        logger.debug(
            "line_created_via_cli",
            x1=x1_val,
            y1=y1_val,
            x2=x2_val,
            y2=y2_val,
            angle=angle,
        )
    except ValueError as e:
        logger.debug("line_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "line-polar",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("x", type=str)
@click.argument("y", type=str)
@click.argument("length", type=str)
@click.argument("direction", type=str)
@_angle_option
@click.pass_context
def create_line_polar(
    ctx: click.Context,
    x: str,
    y: str,
    length: str,
    direction: str,
    angle: float,
) -> None:
    """
    Create a new line from (x,y) with given length and direction (degrees).
    """
    service = _get_shape_service(ctx)

    try:
        x_val = _parse_float(x, "<x>")
        y_val = _parse_float(y, "<y>")
        length_val = _parse_float(length, "<length>")
        dir_val = _parse_float(direction, "<direction>")

        if length_val <= 0:
            raise click.ClickException(
                f"Length must be positive, got {length_val}"
            )

        shape = service.create_line_polar(
            x_val, y_val, length_val, dir_val, rotation=angle
        )
        click.echo(f"✔ Created: {format_shape(shape)}")
        logger.debug(
            "line_polar_created_via_cli",
            x=x_val,
            y=y_val,
            length=length_val,
            direction=dir_val,
            angle=angle,
        )
    except ValueError as e:
        logger.debug("line_polar_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "circle",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("x", type=str)
@click.argument("y", type=str)
@click.argument("radius", type=str)
@_angle_option
@click.pass_context
def create_circle(
    ctx: click.Context,
    x: str,
    y: str,
    radius: str,
    angle: float,
) -> None:
    """
    Create a new circle with center at (x,y) and given radius.
    """
    service = _get_shape_service(ctx)

    try:
        x_val = _parse_float(x, "<x>")
        y_val = _parse_float(y, "<y>")
        radius_val = _parse_float(radius, "<radius>")

        if radius_val <= 0:
            raise click.ClickException(
                f"Radius must be positive, got {radius_val}"
            )

        shape = service.create_circle(x_val, y_val, radius_val, rotation=angle)
        click.echo(f"✔ Created: {format_shape(shape)}")
        logger.debug(
            "circle_created_via_cli",
            x=x_val,
            y=y_val,
            radius=radius_val,
            angle=angle,
        )
    except ValueError as e:
        logger.debug("circle_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "square",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("x", type=str)
@click.argument("y", type=str)
@click.argument("side", type=str)
@_angle_option
@click.pass_context
def create_square(
    ctx: click.Context,
    x: str,
    y: str,
    side: str,
    angle: float,
) -> None:
    """
    Create a new square with center at (x,y) and given side length.
    """
    service = _get_shape_service(ctx)

    try:
        x_val = _parse_float(x, "<x>")
        y_val = _parse_float(y, "<y>")
        side_val = _parse_float(side, "<side>")

        if side_val <= 0:
            raise click.ClickException(
                f"Side length must be positive, got {side_val}"
            )

        shape = service.create_square(x_val, y_val, side_val, rotation=angle)
        click.echo(f"✔ Created: {format_shape(shape)}")
        logger.debug(
            "square_created_via_cli",
            x=x_val,
            y=y_val,
            side=side_val,
            angle=angle,
        )
    except ValueError as e:
        logger.debug("square_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "rectangle",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("x", type=str)
@click.argument("y", type=str)
@click.argument("width", type=str)
@click.argument("height", type=str)
@_angle_option
@click.pass_context
def create_rectangle(
    ctx: click.Context,
    x: str,
    y: str,
    width: str,
    height: str,
    angle: float,
) -> None:
    """
    Create a new rectangle with center at (x,y), width and height.
    """
    service = _get_shape_service(ctx)

    try:
        x_val = _parse_float(x, "<x>")
        y_val = _parse_float(y, "<y>")
        width_val = _parse_float(width, "<width>")
        height_val = _parse_float(height, "<height>")

        if width_val <= 0:
            raise click.ClickException(
                f"Width must be positive, got {width_val}"
            )
        if height_val <= 0:
            raise click.ClickException(
                f"Height must be positive, got {height_val}"
            )

        shape = service.create_rectangle(
            x_val, y_val, width_val, height_val, rotation=angle
        )
        click.echo(f"✔ Created: {format_shape(shape)}")
        logger.debug(
            "rectangle_created_via_cli",
            x=x_val,
            y=y_val,
            width=width_val,
            height=height_val,
            angle=angle,
        )
    except ValueError as e:
        logger.debug("rectangle_creation_failed", error=str(e))
        raise click.ClickException(str(e))


@cli.command(
    "ellipse",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("x", type=str)
@click.argument("y", type=str)
@click.argument("rx", type=str)
@click.argument("ry", type=str)
@_angle_option
@click.pass_context
def create_ellipse(
    ctx: click.Context,
    x: str,
    y: str,
    rx: str,
    ry: str,
    angle: float,
) -> None:
    """
    Create a new ellipse with center at (x,y), horizontal radius rx and vertical radius ry.
    """
    service = _get_shape_service(ctx)

    try:
        x_val = _parse_float(x, "<x>")
        y_val = _parse_float(y, "<y>")
        rx_val = _parse_float(rx, "<rx>")
        ry_val = _parse_float(ry, "<ry>")

        if rx_val <= 0:
            raise click.ClickException(
                f"Horizontal radius must be positive, got {rx_val}"
            )
        if ry_val <= 0:
            raise click.ClickException(
                f"Vertical radius must be positive, got {ry_val}"
            )

        shape = service.create_ellipse(
            x_val, y_val, rx_val, ry_val, rotation=angle
        )
        click.echo(f"✔ Created: {format_shape(shape)}")
        logger.debug(
            "ellipse_created_via_cli",
            x=x_val,
            y=y_val,
            rx=rx_val,
            ry=ry_val,
            angle=angle,
        )
    except ValueError as e:
        logger.debug("ellipse_creation_failed", error=str(e))
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
            click.echo(f"✔ Deleted shape {shape_id}")
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
    click.echo(f"✔ Deleted all {count} shapes")
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
