import json


def sse(evnet: str, data) -> str:
    """Format one Server-Sent Event: an event name line plus a JSON data line."""
    return f"event: {evnet}\ndata: {json.dumps(data)}\n\n"
