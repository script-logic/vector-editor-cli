"""
Console output formatting utilities for CLI.
"""

from uuid import UUID

from src.vector_editor.domain.entities import (
    Circle,
    IShape,
    Line,
    Point,
    Square,
)


def format_shape(shape: IShape) -> str:
    """
    Format a single shape for console output.

    Args:
        shape: The shape to format

    Returns:
        Formatted string representation
    """
    try:
        shape_id = _short_id(shape.id) if hasattr(shape, "id") else "test-id"
    except AttributeError, ValueError:
        shape_id = "test-id"

    if isinstance(shape, Point):
        return (
            f"🟤 Point(ID: {shape_id}, "
            f"x={shape.coordinates.x:.2f}, y={shape.coordinates.y:.2f})"
        )
    if isinstance(shape, Line):
        return (
            f"📏 Line(ID: {shape_id}, "
            f"({shape.start.x:.2f}, {shape.start.y:.2f}) → "
            f"({shape.end.x:.2f}, {shape.end.y:.2f}))"
        )
    if isinstance(shape, Circle):
        return (
            f"⚪ Circle(ID: {shape_id}, "
            f"center=({shape.center.x:.2f}, {shape.center.y:.2f}), "
            f"radius={shape.radius:.2f})"
        )
    if isinstance(shape, Square):
        bottom_right = shape.bottom_right()
        return (
            f"⬛ Square(ID: {shape_id}, "
            f"top_left=({shape.top_left.x:.2f}, {shape.top_left.y:.2f}), "
            f"bottom_right=({bottom_right.x:.2f}, {bottom_right.y:.2f}), "
            f"side={shape.side_length:.2f})"
        )
    return f"Unknown shape: {shape}"


def format_shape_list(shapes: list[IShape]) -> str:
    """
    Format a list of shapes for console output.

    Args:
        shapes: List of shapes to format

    Returns:
        Formatted string with all shapes
    """
    if not shapes:
        return "📭 No shapes created yet."

    lines = [f"📋 Shapes ({len(shapes)} total):"]
    for i, shape in enumerate(shapes, 1):
        lines.append(f"  {i}. {format_shape(shape)}")
    return "\n".join(lines)


def _short_id(uuid_obj: UUID) -> str:
    """Return short version of UUID for display."""
    return str(uuid_obj).split("-")[0]
