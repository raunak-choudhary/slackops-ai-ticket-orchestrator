import os

from ai_api.ai_api.ai_interface import AIInterface
from chat_api.chat_api.chat_interface import ChatInterface


def route_message_to_ai(
    ai_client: AIInterface,
    user_input: str,
    system_prompt: str,
) -> str:
    result = ai_client.generate_response(
        user_input=user_input,
        system_prompt=system_prompt,
        response_schema=None,
    )

    if isinstance(result, dict):
        return str(result)

    return result


def extract_ai_command(message_text: str) -> str | None:
    trigger = "@team4_ai"
    if trigger not in message_text:
        return None

    after_trigger = message_text.split(trigger, 1)[1]
    return after_trigger.strip()


def poll_and_respond_with_ai(
    chat_client: ChatInterface,
    ai_client: AIInterface,
    system_prompt: str,
    limit: int = 10,
) -> None:
    channel_id = os.environ.get("SLACK_CHANNEL_ID")
    if not channel_id:
        raise RuntimeError("SLACK_CHANNEL_ID is not set in the environment")

    messages = chat_client.get_messages(channel_id=channel_id, limit=limit)

    for message in messages:
        command = extract_ai_command(message.content)
        if command is None:
            continue

        response = route_message_to_ai(
            ai_client=ai_client,
            user_input=command,
            system_prompt=system_prompt,
        )

        chat_client.send_message(channel_id=channel_id, content=response)
        break
