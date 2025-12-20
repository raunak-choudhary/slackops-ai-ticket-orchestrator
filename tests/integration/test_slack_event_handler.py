import pytest

from integration_app.slack_entry import SlackEventHandler
from slack_adapter.slack_adapter import SlackServiceClient

pytestmark = pytest.mark.integration

def test_slack_event_handler_accepts_message_event():
    handler = SlackEventHandler(SlackServiceClient())

    payload = {
        "event": {
            "type": "message",
            "text": "ai say OK",
            "channel": "dummy-channel",
        }
    }

    result = handler.handle_event(payload)
    assert result["status"] == "accepted"
