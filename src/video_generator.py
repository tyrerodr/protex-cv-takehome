from pathlib import Path
from typing import Any

import cv2

from config import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    OUTPUT_FPS,
    PERSON_CAR_ROIS,
    RULE_NAME,
)
from event_detector import PersonCarEventDetector
from geometry import enrich_detection_with_position
from visualizer import FrameVisualizer


class VideoGenerator:
    def __init__(
        self,
        canvas_width: int = CANVAS_WIDTH,
        canvas_height: int = CANVAS_HEIGHT,
        output_fps: int = OUTPUT_FPS,
    ) -> None:
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.output_fps = output_fps
        self.visualizer = FrameVisualizer(
            canvas_width=canvas_width,
            canvas_height=canvas_height,
        )
        self.event_detector = PersonCarEventDetector(
            rois=PERSON_CAR_ROIS,
            rule_name=RULE_NAME,
        )

    def generate(
        self,
        annotations: dict[str, Any],
        output_path: Path,
    ) -> list[dict[str, Any]]:
        video_writer = self._create_video_writer(output_path)
        all_events: list[dict[str, Any]] = []

        for frame in annotations["frames"]:
            frame_events = self._process_frame(
                frame=frame,
                annotations=annotations,
                video_writer=video_writer,
            )

            all_events.extend(frame_events)

        video_writer.release()

        return all_events

    def _create_video_writer(self, output_path: Path) -> cv2.VideoWriter:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        return cv2.VideoWriter(
            filename=str(output_path),
            fourcc=fourcc,
            fps=self.output_fps,
            frameSize=(self.canvas_width, self.canvas_height),
        )

    def _process_frame(
        self,
        frame: dict[str, Any],
        annotations: dict[str, Any],
        video_writer: cv2.VideoWriter,
    ) -> list[dict[str, Any]]:
        frame_num = frame["frame_num"]
        timestamp = frame.get("formatted_timestamp", frame["timestamp"])
        frame_width = frame["frame_width"]
        frame_height = frame["frame_height"]

        enriched_detections = [
            enrich_detection_with_position(
                detection=detection,
                frame_width=frame_width,
                frame_height=frame_height,
            )
            for detection in frame["detections"]
        ]

        events = self.event_detector.detect(
            detections=enriched_detections,
            timestamp=timestamp,
            frame_num=frame_num,
            camera_name=annotations["cam_name"],
        )

        canvas = self.visualizer.render_frame(
            frame_num=frame_num,
            timestamp=timestamp,
            rois=PERSON_CAR_ROIS,
            detections=enriched_detections,
            events=events,
        )

        video_writer.write(canvas)

        return events