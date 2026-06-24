from pathlib import Path
import json
from typing import Any
from config import CAMERA_NAME, PERSON_CAR_ROIS, RULE_NAME
from event_detector import detect_person_car_events
from geometry import enrich_detection_with_position


DEFAULT_ANNOTATIONS_PATH = Path("data/sample_annotations.json")


def load_annotations(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Annotations file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    annotations = load_annotations(DEFAULT_ANNOTATIONS_PATH)

    print(f"Loaded {len(annotations)} frames")
    all_events: list[dict[str, Any]] = []

    for frame in annotations:
        frame_num = frame["Frame_num"]
        timestamp = frame["Timestamp"]
        frame_width = frame["Frame_width"]
        frame_height = frame["Frame_height"]

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
            camera_name=CAMERA_NAME,
        )

        all_events.extend(events)

        print(f"\nFrame {frame_num} | Timestamp: {timestamp}")

        for detection in enriched_detections:
            print(
                f"- {detection['class']} "
                f"id={detection['object_id']} "
                f"bbox_pixels={detection['bbox_pixels']} "
                f"point={detection['point']}"
            )

        if events:
            print("Events detected:")
            for event in events:
                print(
                    f"  - {event['rule_name']} | "
                    f"{event['camera_name']} | "
                    f"{event['roi_name']} | "
                    f"timestamp={event['timestamp']}"
                )
        else:
            print("No events detected.")

    print(f"\nTotal events detected: {len(all_events)}")


if __name__ == "__main__":
    main()