from typing import Any


def format_event_as_slack_message(event: dict[str, Any]) -> dict[str, Any]:
    camera_name = event["camera_name"]
    rule_name = event["rule_name"]
    roi_name = event["roi_name"]
    frame_num = event["frame_num"]
    timestamp = event["timestamp"]

    return {
        "text": f"{rule_name} detected in {roi_name}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Safety Event Detected",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Camera:*\n{camera_name}"},
                    {"type": "mrkdwn", "text": f"*Rule:*\n{rule_name}"},
                    {"type": "mrkdwn", "text": f"*ROI:*\n{roi_name}"},
                    {"type": "mrkdwn", "text": f"*Frame:*\n{frame_num}"},
                    {"type": "mrkdwn", "text": f"*Timestamp:*\n{timestamp}"},
                ],
            },
        ],
    }


def format_events_as_slack_messages(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        format_event_as_slack_message(event)
        for event in events
    ]