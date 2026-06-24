from typing import Any

import cv2
import numpy as np

from config import CANVAS_HEIGHT, CANVAS_WIDTH

CLASS_COLORS = {
    "Person": (0, 255, 0), #Green
    "Car": (255, 0, 0), #Blue
    "Truck": (180, 180, 180), #Gray
}

DEFAULT_COLOR = (255, 255, 255) #White
ROI_COLOR = (0, 255, 255) #Yellow
EVENT_COLOR = (0, 0, 255) #Red


def create_black_canvas() -> np.ndarray:
    return np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), dtype=np.uint8)

def draw_rois(
    canvas: np.ndarray,
    rois: dict[str, list[tuple[int, int]]],
    triggered_roi_names: set[str] | None = None,
) -> None:
    if triggered_roi_names is None:
        triggered_roi_names = set()

    for roi_name, roi_points in rois.items():
        points = np.array(roi_points, dtype=np.int32).reshape((-1, 1, 2))

        color = EVENT_COLOR if roi_name in triggered_roi_names else ROI_COLOR
        thickness = 5 if roi_name in triggered_roi_names else 2

        cv2.polylines(
            img=canvas,
            pts=[points],
            isClosed=True,
            color=color,
            thickness=thickness,
        )

        label_position = roi_points[0]
        cv2.putText(
            img=canvas,
            text=roi_name.replace("Person Car Region of Interest ", "ROI "),
            org=(label_position[0], label_position[1] - 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,
            color=color,
            thickness=2,
            lineType=cv2.LINE_AA,
        )


def draw_detections(
    canvas: np.ndarray,
    detections: list[dict[str, Any]],
) -> None:
    for detection in detections:
        object_class = detection["class"]
        object_id = detection["object_id"]
        point = detection["point"]

        color = CLASS_COLORS.get(object_class, DEFAULT_COLOR)

        cv2.circle(
            img=canvas,
            center=point,
            radius=8,
            color=color,
            thickness=-1,
        )

        cv2.putText(
            img=canvas,
            text=f"{object_class} #{object_id}",
            org=(point[0] + 10, point[1] - 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=color,
            thickness=2,
            lineType=cv2.LINE_AA,
        )


def draw_frame_metadata(
    canvas: np.ndarray,
    frame_num: int,
    timestamp: int | float,
) -> None:
    cv2.putText(
        img=canvas,
        text=f"Frame: {frame_num} | Timestamp: {timestamp}",
        org=(30, 50),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.80,
        color=(255, 255, 255),
        thickness=2,
        lineType=cv2.LINE_AA,
    )


def draw_event_indicator(
    canvas: np.ndarray,
    events: list[dict[str, Any]],
) -> None:
    if not events:
        return

    cv2.rectangle(
        img=canvas,
        pt1=(20, 80),
        pt2=(690, 170),
        color=EVENT_COLOR,
        thickness=-1,
    )

    cv2.putText(
        img=canvas,
        text="EVENT TRIGGERED: Person + Car inside ROI",
        org=(40, 135),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.90,
        color=(255, 255, 255),
        thickness=3,
        lineType=cv2.LINE_AA,
    )