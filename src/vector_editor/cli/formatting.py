"""
Console output formatting utilities for CLI.
"""

from uuid import UUID

from src.vector_editor.domain import PlacedShape
from src.vector_editor.domain.geometry import (
    CircleGeometry,
    EllipseGeometry,
    LineGeometry,
    PointGeometry,
    RectangleGeometry,
    SquareGeometry,
)


def format_shape(shape: PlacedShape) -> str:
    """
    Format a placed shape for console output.

    Args:
        shape: The placed shape to format

    Returns:
        Formatted string representation
    """
    shape_id = _short_id(shape.id)
    geometry = shape.render()
    rotation = shape.transform.rotation_deg

    if isinstance(geometry, PointGeometry):
        return (
            f"⋅ Point(ID: {shape_id}, "
            f"x={geometry.coordinates.x:.2f}, y={geometry.coordinates.y:.2f}, "
            f"rot={rotation:.1f}°)"
        )
    if isinstance(geometry, LineGeometry):
        return (
            f"─ Line(ID: {shape_id}, "
            f"({geometry.start.x:.2f}, {geometry.start.y:.2f}) → "
            f"({geometry.end.x:.2f}, {geometry.end.y:.2f}), "
            f"rot={rotation:.1f}°)"
        )
    if isinstance(geometry, CircleGeometry):
        return (
            f"◯ Circle(ID: {shape_id}, "
            f"center=({geometry.center.x:.2f}, {geometry.center.y:.2f}), "
            f"radius={geometry.radius:.2f}, rot={rotation:.1f}°)"
        )
    if isinstance(geometry, SquareGeometry):
        return (
            f"☐ Square(ID: {shape_id}, "
            f"center=({geometry.center.x:.2f}, {geometry.center.y:.2f}), "
            f"side={geometry.side_length:.2f}, rot={rotation:.1f}°)"
        )
    if isinstance(geometry, RectangleGeometry):
        return (
            f"▭ Rectangle(ID: {shape_id}, "
            f"center=({geometry.center.x:.2f}, {geometry.center.y:.2f}), "
            f"width={geometry.width:.2f}, height={geometry.height:.2f}, "
            f"rot={rotation:.1f}°)"
        )
    if isinstance(geometry, EllipseGeometry):
        return (
            f"𝟶 Ellipse(ID: {shape_id}, "
            f"center=({geometry.center.x:.2f}, {geometry.center.y:.2f}), "
            f"rx={geometry.radius_x:.2f}, ry={geometry.radius_y:.2f}, "
            f"rot={rotation:.1f}°)"
        )
    return f"Unknown shape: {geometry}"


def format_shape_list(shapes: list[PlacedShape]) -> str:
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
