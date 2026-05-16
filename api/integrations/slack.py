import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

_client: WebClient | None = None

def get_client() -> WebClient:
    global _client
    if _client is None:
        _client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    return _client

def send_message(channel: str, text: str) -> dict:
    try:
        response = get_client().chat_postMessage(channel=channel, text=text)
        return {"ok": True, "ts": response["ts"]}
    except SlackApiError as e:
        return {"ok": False, "error": str(e)}

def get_users() -> list[dict]:
    try:
        response = get_client().users_list()
        return [
            {"id": u["id"], "name": u["name"], "real_name": u.get("real_name", "")}
            for u in response["members"]
            if not u.get("is_bot") and not u.get("deleted")
        ]
    except SlackApiError:
        return []
