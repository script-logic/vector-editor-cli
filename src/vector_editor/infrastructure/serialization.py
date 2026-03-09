"""
JSON serialization for domain shapes.
"""

import uuid
from typing import Any

from src.vector_editor.domain import PlacedShape
from src.vector_editor.domain.definitions import (
    CircleDefinition,
    EllipseDefinition,
    LineDefinition,
    LineRepresentation,
    PointDefinition,
    RectangleDefinition,
    SquareDefinition,
)
from src.vector_editor.domain.primitives import Coordinates, Transform
from src.vector_editor.logger import get_logger

logger = get_logger(__name__)


def shape_to_dict(shape: PlacedShape) -> dict[str, Any]:
    """
    Convert a PlacedShape to a JSON-serializable dictionary.
    """
    definition = shape.definition
    def_type = _get_definition_type(definition)

    definition_dict: dict[str, Any] = {
        "type": def_type,
    }

    if isinstance(definition, PointDefinition):
        definition_dict["coordinates"] = {
            "x": definition.coordinates.x,
            "y": definition.coordinates.y,
        }
    elif isinstance(definition, LineDefinition):
        definition_dict["representation"] = definition.representation.value

        if definition.representation == LineRepresentation.TWO_POINTS:
            if definition.start is None or definition.end is None:
                raise ValueError("Line coordinates value error (None)")
            definition_dict["start"] = {
                "x": definition.start.x,
                "y": definition.start.y,
            }
            definition_dict["end"] = {
                "x": definition.end.x,
                "y": definition.end.y,
            }
        elif definition.representation == LineRepresentation.POLAR:
            if definition.origin is None:
                raise ValueError(
                    "Line origin is None for POLAR representation"
                )
            if definition.length is None or definition.angle_deg is None:
                raise ValueError(
                    "Line length or angle is None for POLAR representation"
                )
            definition_dict["origin"] = {
                "x": definition.origin.x,
                "y": definition.origin.y,
            }
            definition_dict["length"] = definition.length
            definition_dict["angle_deg"] = definition.angle_deg
        else:
            raise ValueError(
                f"Unknown line representation: {definition.representation}"
            )
    elif isinstance(definition, CircleDefinition):
        definition_dict["center"] = {
            "x": definition.center.x,
            "y": definition.center.y,
        }
        definition_dict["radius"] = definition.radius
    elif isinstance(definition, SquareDefinition):
        definition_dict["center"] = {
            "x": definition.center.x,
            "y": definition.center.y,
        }
        definition_dict["side_length"] = definition.side_length
    elif isinstance(definition, RectangleDefinition):
        definition_dict["center"] = {
            "x": definition.center.x,
            "y": definition.center.y,
        }
        definition_dict["width"] = definition.width
        definition_dict["height"] = definition.height
    elif isinstance(definition, EllipseDefinition):
        definition_dict["center"] = {
            "x": definition.center.x,
            "y": definition.center.y,
        }
        definition_dict["radius_x"] = definition.radius_x
        definition_dict["radius_y"] = definition.radius_y
    else:
        raise TypeError(f"Unknown definition type: {type(definition)}")

    data: dict[str, Any] = {
        "id": str(shape.id),
        "transform": {
            "rotation_deg": shape.transform.rotation_deg,
        },
        "definition": definition_dict,
    }
    return data


def dict_to_shape(data: dict[str, Any]) -> PlacedShape:
    """
    Reconstruct a PlacedShape from a dictionary.
    Raises ValueError if data is malformed.
    """
    try:
        shape_id = uuid.UUID(data["id"])
        transform = Transform(rotation_deg=data["transform"]["rotation_deg"])
        def_data = data["definition"]
        def_type = def_data["type"]

        if def_type == "point":
            coords = Coordinates(
                x=def_data["coordinates"]["x"],
                y=def_data["coordinates"]["y"],
            )
            definition = PointDefinition(coordinates=coords)
        elif def_type == "line":
            rep = def_data.get("representation", "two_points")
            if rep == "two_points":
                start = Coordinates(
                    x=def_data["start"]["x"], y=def_data["start"]["y"]
                )
                end = Coordinates(
                    x=def_data["end"]["x"], y=def_data["end"]["y"]
                )
                definition = LineDefinition.from_points(start, end)
            elif rep == "polar":
                origin = Coordinates(
                    x=def_data["origin"]["x"], y=def_data["origin"]["y"]
                )
                length = def_data["length"]
                angle_deg = def_data["angle_deg"]
                definition = LineDefinition.from_polar(
                    origin, length, angle_deg
                )
            else:
                raise ValueError(f"Unknown line representation: {rep}")
        elif def_type == "circle":
            center = Coordinates(
                x=def_data["center"]["x"], y=def_data["center"]["y"]
            )
            definition = CircleDefinition(
                center=center, radius=def_data["radius"]
            )
        elif def_type == "square":
            center = Coordinates(
                x=def_data["center"]["x"], y=def_data["center"]["y"]
            )
            definition = SquareDefinition(
                center=center, side_length=def_data["side_length"]
            )
        elif def_type == "rectangle":
            center = Coordinates(
                x=def_data["center"]["x"], y=def_data["center"]["y"]
            )
            definition = RectangleDefinition(
                center=center,
                width=def_data["width"],
                height=def_data["height"],
            )
        elif def_type == "ellipse":
            center = Coordinates(
                x=def_data["center"]["x"], y=def_data["center"]["y"]
            )
            definition = EllipseDefinition(
                center=center,
                radius_x=def_data["radius_x"],
                radius_y=def_data["radius_y"],
            )
        else:
            raise ValueError(f"Unknown shape type: {def_type}")

        return PlacedShape(
            definition=definition, transform=transform, id=shape_id
        )
    except (KeyError, ValueError, TypeError) as e:
        logger.error("failed_to_deserialize_shape", error=str(e))
        raise ValueError(f"Invalid shape data: {e}") from e


def _get_definition_type(definition: Any) -> str:
    """Return string type identifier for a definition."""
    if isinstance(definition, PointDefinition):
        return "point"
    if isinstance(definition, LineDefinition):
        return "line"
    if isinstance(definition, CircleDefinition):
        return "circle"
    if isinstance(definition, SquareDefinition):
        return "square"
    if isinstance(definition, RectangleDefinition):
        return "rectangle"
    if isinstance(definition, EllipseDefinition):
        return "ellipse"
    raise ValueError(f"Unknown definition type: {type(definition)}")
