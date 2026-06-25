from typing import Any

from geometry import is_point_inside_roi

class PersonCarEventDetector:
    def __init__(
        self,
        rois: dict[str, list[tuple[int, int]]],
        rule_name: str,
    ) -> None:
        self.rois = rois
        self.rule_name = rule_name

    def detect(
        self,
        detections: list[dict[str, Any]],
        timestamp: int | float | str,
        frame_num: int,
        camera_name: str,
    ) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []

        for roi_name, roi_points in self.rois.items():
            classes_inside_roi = self._find_classes_inside_roi(
                detections=detections,
                roi_points=roi_points,
            )

            has_person = "person" in classes_inside_roi
            has_car = "car" in classes_inside_roi

            if has_person and has_car:
                events.append(
                    {
                        "timestamp": timestamp,
                        "frame_num": frame_num,
                        "rule_name": self.rule_name,
                        "camera_name": camera_name,
                        "roi_name": roi_name,
                        "classes_inside_roi": sorted(classes_inside_roi),
                    }
                )

        return events

    def _find_classes_inside_roi(
        self,
        detections: list[dict[str, Any]],
        roi_points: list[tuple[int, int]],
    ) -> set[str]:
        classes_inside_roi: set[str] = set()

        for detection in detections:
            object_class = detection["class"]
            point = detection["point"]

            if is_point_inside_roi(point=point, roi_points=roi_points):
                classes_inside_roi.add(object_class)

        return classes_inside_roi