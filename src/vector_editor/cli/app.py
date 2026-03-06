"""
CLI application for vector editor.
"""

from uuid import UUID

import click
from src.vector_editor.application import ShapeService
from src.vector_editor.logger import get_logger

from .formatting import format_shape, format_shape_list

logger = get_logger(__name__)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Vector Editor CLI - Create and manage geometric shapes.

    This tool allows you to create points, lines, circles, and squares,
    list them, and delete them.
    """
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


def _get_service(ctx: click.Context) -> ShapeService:
    """Get ShapeService from context."""
    service = ctx.obj.get("service")
    if service is None:
        raise click.ClickException("Service not initialized. This is a bug.")
    return service


@cli.command("point")
@click.argument("x", type=float)
@click.argument("y", type=float)
@click.pass_context
def create_point(ctx: click.Context, x: float, y: float) -> None:
    """Create a new point at coordinates (X, Y)."""
    service = _get_service(ctx)
    try:
        point = service.create_point(x, y)
        click.echo(f"✅ Created: {format_shape(point)}")
        logger.debug("point_created_via_cli", x=x, y=y)
    except ValueError as e:
        logger.error("point_creation_failed", x=x, y=y, error=str(e))
        raise click.ClickException(str(e))


@cli.command("line")
@click.argument("x1", type=float)
@click.argument("y1", type=float)
@click.argument("x2", type=float)
@click.argument("y2", type=float)
@click.pass_context
def create_line(
    ctx: click.Context,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> None:
    """Create a new line from (X1, Y1) to (X2, Y2)."""
    service = _get_service(ctx)
    try:
        line = service.create_line(x1, y1, x2, y2)
        click.echo(f"✅ Created: {format_shape(line)}")
        logger.debug("line_created_via_cli", x1=x1, y1=y1, x2=x2, y2=y2)
    except ValueError as e:
        logger.error(
            "line_creation_failed", x1=x1, y1=y1, x2=x2, y2=y2, error=str(e)
        )
        raise click.ClickException(str(e))


@cli.command("circle")
@click.argument("x", type=float)
@click.argument("y", type=float)
@click.argument("radius", type=float)
@click.pass_context
def create_circle(
    ctx: click.Context, x: float, y: float, radius: float
) -> None:
    """Create a new circle with center at (X, Y) and given RADIUS."""
    service = _get_service(ctx)
    try:
        circle = service.create_circle(x, y, radius)
        click.echo(f"✅ Created: {format_shape(circle)}")
        logger.debug("circle_created_via_cli", x=x, y=y, radius=radius)
    except ValueError as e:
        logger.error(
            "circle_creation_failed", x=x, y=y, radius=radius, error=str(e)
        )
        raise click.ClickException(str(e))


@cli.command("square")
@click.argument("x", type=float)
@click.argument("y", type=float)
@click.argument("side_length", type=float)
@click.pass_context
def create_square(
    ctx: click.Context,
    x: float,
    y: float,
    side_length: float,
) -> None:
    """
    Create a new square with top-left corner at (X, Y) and given SIDE_LENGTH.
    """
    service = _get_service(ctx)
    try:
        square = service.create_square(x, y, side_length)
        click.echo(f"✅ Created: {format_shape(square)}")
        logger.debug(
            "square_created_via_cli", x=x, y=y, side_length=side_length
        )
    except ValueError as e:
        logger.error(
            "square_creation_failed",
            x=x,
            y=y,
            side_length=side_length,
            error=str(e),
        )
        raise click.ClickException(str(e))


@cli.command("list")
@click.pass_context
def list_shapes(ctx: click.Context) -> None:
    """List all created shapes."""
    service = _get_service(ctx)
    shapes = service.get_all_shapes()
    click.echo(format_shape_list(shapes))
    logger.debug("shapes_listed_via_cli", count=len(shapes))


@cli.command("delete")
@click.argument("shape_id", type=str)
@click.pass_context
def delete_shape(ctx: click.Context, shape_id: str) -> None:
    """Delete a shape by its ID (first 8 characters are enough)."""
    service = _get_service(ctx)
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
    service = _get_service(ctx)
    count = service.count_shapes()
    service.clear_all()
    click.echo(f"✅ Deleted all {count} shapes")
    logger.debug("all_shapes_cleared_via_cli", count=count)


@cli.command("count")
@click.pass_context
def count_shapes(ctx: click.Context) -> None:
    """Show total number of shapes."""
    service = _get_service(ctx)
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
