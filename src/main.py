from datetime import datetime
from pathlib import Path
import json
from typing import Any

from slack_notifier import SlackNotifier
from slack_formatter import format_events_as_slack_messages
from video_generator import VideoGenerator


DEFAULT_ANNOTATIONS_PATH = Path("data/annotations.json")
DEFAULT_OUTPUT_VIDEO_PATH = Path("outputs/output.mp4")


def format_timestamp(timestamp_ms: int | float) -> str:
    timestamp_seconds = timestamp_ms / 1000
    return datetime.fromtimestamp(timestamp_seconds).strftime("%Y-%m-%d %H:%M:%S")


def load_annotations(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Annotations file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        annotations = json.load(file)

    annotations["frames"] = [
        {
            **frame,
            "formatted_timestamp": format_timestamp(frame["timestamp"]),
        }
        for frame in annotations["frames"]
    ]

    return annotations


def main() -> None:
    video_generator = VideoGenerator()
    slack_notifier = SlackNotifier()

    annotations = load_annotations(DEFAULT_ANNOTATIONS_PATH)

    events = video_generator.generate(
        annotations=annotations,
        output_path=DEFAULT_OUTPUT_VIDEO_PATH,
    )

    slack_messages = format_events_as_slack_messages(events)
    slack_notifier.send_messages(slack_messages)

    print(f"Total events detected: {len(events)}")
    print(f"Video saved to: {DEFAULT_OUTPUT_VIDEO_PATH}")


if __name__ == "__main__":
    main()