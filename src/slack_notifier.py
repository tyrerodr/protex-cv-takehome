import os
from pprint import pprint
from typing import Any

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


load_dotenv()

class SlackNotifier:
    def __init__(self) -> None:
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")
        self.client = self._create_client()

    def _create_client(self) -> WebClient | None:
        if not self.bot_token:
            return None

        return WebClient(token=self.bot_token)

    def is_configured(self) -> bool:
        return self.client is not None and self.channel_id is not None

    def send_message(self, message: dict[str, Any]) -> bool:
        if not self.is_configured():
            print("Slack is not configured. Printing formatted message instead.")
            pprint(message)
            return False

        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=message["text"],
                blocks=message["blocks"],
            )
            return True

        except SlackApiError as error:
            print(f"Failed to send Slack message: {error.response['error']}")
            return False

    def send_messages(self, messages: list[dict[str, Any]]) -> None:
        for message in messages:
            self.send_message(message)