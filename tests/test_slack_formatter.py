from slack_formatter import format_event_as_slack_message


def test_formats_event_as_slack_message():
    event = {
        "camera_name": "Test Camera",
        "rule_name": "Person and Car inside ROI",
        "roi_name": "Test ROI",
        "frame_num": 1,
        "timestamp": 1000,
    }

    message = format_event_as_slack_message(event)

    assert message["text"] == "Person and Car inside ROI detected in Test ROI"
    assert "blocks" in message
    assert message["blocks"][0]["type"] == "header"
    assert message["blocks"][0]["text"]["text"] == "Safety Event Detected"