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
from event_detector import detect_person_car_events
from geometry import enrich_detection_with_position
from visualizer import (
    create_black_canvas,
    draw_detections,
    draw_event_indicator,
    draw_frame_metadata,
    draw_rois,
)


def create_video_writer(output_path: Path) -> cv2.VideoWriter:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    return cv2.VideoWriter(
        filename=str(output_path),
        fourcc=fourcc,
        fps=OUTPUT_FPS,
        frameSize=(CANVAS_WIDTH, CANVAS_HEIGHT),
    )


def generate_visualization_video(
    annotations: list[dict[str, Any]],
    output_path: Path,
) -> list[dict[str, Any]]:
    video_writer = create_video_writer(output_path)
    all_events: list[dict[str, Any]] = []

    for frame in annotations["frames"]:
        frame_num = frame["frame_num"]
        timestamp = frame["timestamp"]
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

        events = detect_person_car_events(
            detections=enriched_detections,
            rois=PERSON_CAR_ROIS,
            timestamp=timestamp,
            frame_num=frame_num,
            rule_name=RULE_NAME,
            camera_name=annotations["cam_name"],
        )

        all_events.extend(events)

        triggered_roi_names = {
            event["roi_name"]
            for event in events
        }

        canvas = create_black_canvas()

        draw_rois(
            canvas=canvas,
            rois=PERSON_CAR_ROIS,
            triggered_roi_names=triggered_roi_names,
        )
        draw_detections(
            canvas=canvas,
            detections=enriched_detections,
        )
        draw_frame_metadata(
            canvas=canvas,
            frame_num=frame_num,
            timestamp=timestamp,
        )
        draw_event_indicator(
            canvas=canvas,
            events=events,
        )

        video_writer.write(canvas)

    video_writer.release()

    return all_events