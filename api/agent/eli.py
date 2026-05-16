import os
import anthropic
from typing import Generator

_client: anthropic.Anthropic | None = None

SYSTEM_PROMPT = """You are Eli, a virtual employee at Vizio AI. You are helpful, professional, and proactive.

You can:
- Answer questions about the team and company
- Help with tasks and analysis
- Clean and interpret data from APIs
- Send Slack messages to team members
- Query and update the company database

Always be concise, friendly, and action-oriented. When you take an action (like sending a Slack message or saving data), confirm what you did."""

def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client

def chat(messages: list[dict], stream: bool = False):
    if stream:
        return _stream(messages)
    response = get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text

def _stream(messages: list[dict]) -> Generator[str, None, None]:
    with get_client().messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
