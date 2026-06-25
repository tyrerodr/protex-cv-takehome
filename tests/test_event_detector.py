from event_detector import detect_person_car_events


def test_detects_person_and_car_inside_same_roi() -> None:
    detections = [
        {
            "class": "person",
            "point": (100, 100),
        },
        {
            "class": "car",
            "point":  (200, 200)
        },
    ]

    rois = {
    "Test ROI": [
        (0, 0),
        (300, 0),
        (300, 300),
        (0, 300),
        ]
    }

    events = detect_person_car_events(
        detections=detections,
        rois=rois,
        timestamp=1000,
        frame_num=1,
        rule_name="Person and Car inside ROI",
        camera_name="Test Camera",
    )

    assert len(events) == 1
    assert events[0]["roi_name"] == "Test ROI"
    assert events[0]["frame_num"] == 1
    assert events[0]["camera_name"] == "Test Camera"


def test_does_not_detect_event_with_only_person() -> None:
    detections = [
        {
            "class": "Person",
            "point": (100, 100),
        }
    ]

    rois = {
        "Test ROI": [
            (0, 0),
            (300, 0),
            (300, 300),
            (0, 300),
        ]
    }

    events = detect_person_car_events(
        detections=detections,
        rois=rois,
        timestamp=1000,
        frame_num=1,
        rule_name="Person and Car inside ROI",
        camera_name="Test Camera",
    )

    assert len(events) == 0
    assert all(event["roi_name"] != "Test ROI" for event in events)
