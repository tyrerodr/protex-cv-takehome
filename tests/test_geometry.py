from geometry import enrich_detection_with_position

def test_enrich_detection_with_bottom_center_position():
    detection = {
        "class": "Person",
        "bbox": [100, 200, 300, 500],
    }

    enriched_detection = enrich_detection_with_position(
        detection=detection,
        frame_width=1920,
        frame_height=1080,
    )

    expected_x = 100 * 1920
    expected_y = 200 * 1080
    expected_width = 300 * 1920
    expected_height = 500 * 1080

    assert "bbox_pixels" in enriched_detection
    assert "point" in enriched_detection

    assert enriched_detection["bbox_pixels"] == (
        expected_x,
        expected_y,
        expected_width,
        expected_height,
    )

    assert enriched_detection["point"] == (
        expected_x + expected_width // 2,
        expected_y + expected_height,
    )