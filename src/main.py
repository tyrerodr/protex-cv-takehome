from pathlib import Path
import json
from typing import Any


DEFAULT_ANNOTATIONS_PATH = Path("data/sample_annotations.json")


def load_annotations(path: Path) -> list[dict[str, Any]]:
    
    if not path.exists():
        raise FileNotFoundError(f"Annotations file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    annotations = load_annotations(DEFAULT_ANNOTATIONS_PATH)

    print(f"Loaded {len(annotations)} frames")

    for frame in annotations:
        frame_num = frame["Frame_num"]
        timestamp = frame["Timestamp"]
        detections = frame["detections"]

        print(
            f"Frame {frame_num} | Timestamp: {timestamp} | "
            f"Detections: {len(detections)}"
        )


if __name__ == "__main__":
    main()