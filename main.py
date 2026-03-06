"""
Vector Editor CLI entry point.
"""

import click
from src.vector_editor.application.services import ShapeService
from src.vector_editor.cli import cli
from src.vector_editor.config import get_config
from src.vector_editor.infrastructure.repositories import (
    InMemoryShapeRepository,
)
from src.vector_editor.logger import get_logger, setup_logging

logger = get_logger(__name__)


def main() -> None:
    """Application entry point."""
    config = get_config()

    setup_logging(config.logger_adapter)
    logger = get_logger("main.py")
    logger.debug("application_started", config=config.logger.model_dump())

    repository = InMemoryShapeRepository()
    shape_service = ShapeService(repository)

    click.echo("\n🚀 Vector Editor CLI started.")
    click.echo(
        "\nAvailable commands:"
        "\npoint <x> <y>"
        "\nline <start_x> <start_y> <end_x> <end_y>"
        "\ncircle <center_x> <center_y> <radius>"
        "\nsquare <top_left_x> <top_left_y> <size>"
        "\nlist"
        "\ndelete <id>"
        "\nclear"
        "\ncount"
    )
    click.echo("\nExample:\nline -56 65.7 0 -7")
    click.echo("\nType 'help <command>' for more info.\nType 'q' to quit.\n")

    ctx = click.Context(cli)
    ctx.obj = {"service": shape_service}

    while True:
        try:
            command = input("vector> ").strip()

            if command.lower() in ("exit", "quit", "q"):
                click.echo("👋 Goodbye!")
                break

            if not command:
                continue

            args = command.split()
            cli.main(
                args=args,
                obj={"service": shape_service},
                prog_name="vector-editor",
                standalone_mode=False,
            )
        except click.exceptions.Exit:
            pass
        except click.exceptions.ClickException as e:
            click.echo(f"Error: {e}", err=True)
        except KeyboardInterrupt:
            click.echo()
            continue
        except Exception as e:
            logger.exception("unhandled_exception", error=str(e))
            click.echo(f"Unexpected error: {e}", err=True)


if __name__ == "__main__":
    main()
