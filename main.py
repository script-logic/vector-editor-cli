"""
Vector Editor CLI entry point.
"""

import sys

import click
from src.vector_editor.application.services import ShapeService
from src.vector_editor.cli import cli
from src.vector_editor.config import get_config
from src.vector_editor.infrastructure.repositories import (
    InMemoryShapeRepository,
)
from src.vector_editor.logger import get_logger, setup_logging


def main() -> None:
    """Application entry point."""
    config = get_config()
    setup_logging(config.logger_adapter)
    logger = get_logger("main.py")
    logger.debug("application_started", config=config.logger.model_dump())

    repository = InMemoryShapeRepository()
    shape_service = ShapeService(repository)
    ctx_obj: dict[str, object] = {"shape_service": shape_service}

    click.echo("\n🚀 Vector Editor CLI started.")
    click.echo(
        "\nAvailable commands:"
        "\npoint <x> <y>"
        "\nline <start_x> <start_y> <end_x> <end_y>"
        "\ncircle <center_x> <center_y> <radius>"
        "\nsquare <top_left_x> <top_left_y> <side_length>"
        "\nlist"
        "\ndelete <id>"
        "\nclear"
        "\ncount"
    )
    click.echo("\nExample:\nline -56 65.7 0 -7")
    click.echo("\nType 'help <command>' for more info.\nType 'q' to quit.\n")

    while True:
        try:
            command = input("command: ").strip()

            if command.lower() in ("exit", "quit", "q"):
                click.echo("👋 Goodbye!")
                break

            if not command:
                click.echo(
                    "Type 'help' for available commands or 'q' to quit."
                )
                continue

            cli.main(
                args=command.split(),
                obj=ctx_obj,
                standalone_mode=False,
            )
        except click.exceptions.Exit:
            pass
        except click.exceptions.ClickException as e:
            click.echo(f"Error: {e}", err=True)
        except KeyboardInterrupt:
            click.echo("Type 'q' to quit.")
            continue
        except Exception as e:
            logger.exception("unhandled_exception", error=str(e))
            click.echo(f"Unexpected error: {e}", err=True)
            sys.exit()


if __name__ == "__main__":
    main()
