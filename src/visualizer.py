from typing import Any

import cv2
import numpy as np

from config import CANVAS_HEIGHT, CANVAS_WIDTH

class FrameVisualizer:
    CLASS_COLORS = {
        "person": (0, 255, 0),      # Green
        "car": (255, 0, 0),         # Blue
        "truck": (180, 180, 180),   # Gray
    }

    DEFAULT_COLOR = (255, 255, 255)  # White
    ROI_COLOR = (0, 255, 255)        # Yellow
    EVENT_COLOR = (0, 0, 255)        # Red

    def __init__(
        self,
        canvas_width: int = CANVAS_WIDTH,
        canvas_height: int = CANVAS_HEIGHT,
    ) -> None:
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def create_black_canvas(self) -> np.ndarray:
        return np.zeros(
            (self.canvas_height, self.canvas_width, 3),
            dtype=np.uint8,
        )

    def draw_rois(
        self,
        canvas: np.ndarray,
        rois: dict[str, list[tuple[int, int]]],
        triggered_roi_names: set[str] | None = None,
    ) -> None:
        if triggered_roi_names is None:
            triggered_roi_names = set()

        for roi_name, roi_points in rois.items():
            points = np.array(roi_points, dtype=np.int32).reshape((-1, 1, 2))

            color = self.EVENT_COLOR if roi_name in triggered_roi_names else self.ROI_COLOR
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
                text=self._format_roi_label(roi_name),
                org=(label_position[0], label_position[1] - 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8,
                color=color,
                thickness=2,
                lineType=cv2.LINE_AA,
            )

    def draw_detections(
        self,
        canvas: np.ndarray,
        detections: list[dict[str, Any]],
    ) -> None:
        for detection in detections:
            object_class = detection["class"].lower()
            object_id = detection["object_id"]
            point = detection["point"]

            color = self.CLASS_COLORS.get(object_class, self.DEFAULT_COLOR)

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
        self,
        canvas: np.ndarray,
        frame_num: int,
        timestamp: int | float | str,
    ) -> None:
        cv2.putText(
            img=canvas,
            text=f"Frame: {frame_num} | Timestamp: {timestamp}",
            org=(30, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.80,
            color=self.DEFAULT_COLOR,
            thickness=2,
            lineType=cv2.LINE_AA,
        )

    def draw_event_indicator(
        self,
        canvas: np.ndarray,
        events: list[dict[str, Any]],
    ) -> None:
        if not events:
            return

        cv2.rectangle(
            img=canvas,
            pt1=(20, 80),
            pt2=(690, 170),
            color=self.EVENT_COLOR,
            thickness=-1,
        )

        cv2.putText(
            img=canvas,
            text="EVENT TRIGGERED: Person + Car inside ROI",
            org=(40, 135),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.90,
            color=self.DEFAULT_COLOR,
            thickness=3,
            lineType=cv2.LINE_AA,
        )

    def _format_roi_label(self, roi_name: str) -> str:
        return roi_name.replace("Person Car Region of Interest ", "ROI ")
    
    def render_frame(
        self,
        frame_num: int,
        timestamp: int | float | str,
        rois: dict[str, list[tuple[int, int]]],
        detections: list[dict[str, Any]],
        events: list[dict[str, Any]],
    ) -> np.ndarray:
        triggered_roi_names = {
            event["roi_name"]
            for event in events
        }

        canvas = self.create_black_canvas()

        self.draw_rois(
            canvas=canvas,
            rois=rois,
            triggered_roi_names=triggered_roi_names,
        )

        self.draw_detections(
            canvas=canvas,
            detections=detections,
        )

        self.draw_frame_metadata(
            canvas=canvas,
            frame_num=frame_num,
            timestamp=timestamp,
        )

        self.draw_event_indicator(
            canvas=canvas,
            events=events,
        )

        return canvas