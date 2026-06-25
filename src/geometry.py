from typing import Any

from shapely.geometry import Point, Polygon

def extract_bbox_values(
    bbox: list[float] | dict[str, float],
) -> tuple[float, float, float, float]:
    if isinstance(bbox, dict):
        return (
            bbox["left"],
            bbox["top"],
            bbox["width"],
            bbox["height"],
        )

    x, y, width, height = bbox
    return x, y, width, height


def fractional_bbox_to_pixels(
    bbox: list[float] | dict[str, float],
    frame_width: int,
    frame_height: int,
) -> tuple[int, int, int, int]:
    x, y, width, height = extract_bbox_values(bbox)

    return (
        int(x * frame_width),
        int(y * frame_height),
        int(width * frame_width),
        int(height * frame_height),
    )


def get_bbox_bottom_center(
    bbox_pixels: tuple[int, int, int, int],
) -> tuple[int, int]:
    x, y, width, height = bbox_pixels

    point_x = x + width // 2
    point_y = y + height

    return point_x, point_y


def is_point_inside_roi(
    point: tuple[int, int],
    roi_points: list[tuple[int, int]],
) -> bool:
    polygon = Polygon(roi_points)
    shapely_point = Point(point)

    return polygon.contains(shapely_point) or polygon.touches(shapely_point)

def enrich_detection_with_position(
    detection: dict[str, Any],
    frame_width: int,
    frame_height: int,
) -> dict[str, Any]:
    bbox_pixels = fractional_bbox_to_pixels(
        bbox=detection["bbox"],
        frame_width=frame_width,
        frame_height=frame_height,
    )

    point = get_bbox_bottom_center(bbox_pixels)

    return {
        **detection,
        "class": detection["class"].lower(),
        "bbox_pixels": bbox_pixels,
        "point": point,
    }