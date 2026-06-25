import os
from typing import Any
from pprint import pprint
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

def create_slack_client() -> WebClient | None:
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

    if not slack_bot_token:
        return None

    return WebClient(token=slack_bot_token)


def send_slack_message(
    client: WebClient,
    channel_id: str,
    message: dict[str, Any],
) -> bool:
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=message["text"],
            blocks=message["blocks"],
        )
        return True

    except SlackApiError as error:
        print(f"Failed to send Slack message: {error.response['error']}")
        return False


def send_slack_messages(
    messages: list[dict[str, Any]],
) -> None:
    slack_channel_id = os.getenv("SLACK_CHANNEL_ID")
    client = create_slack_client()

    if client is None or not slack_channel_id:
        print("Slack is not configured. Printing formatted messages instead.")

        for message in messages:
            pprint(message)

        return

    for message in messages:
        send_slack_message(
            client=client,
            channel_id=slack_channel_id,
            message=message,
        )