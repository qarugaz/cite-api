import time

import httpx

from app.auth.auth import generate_hmac_signature
from app.config.config import API_KEY
from app.logging.logging_config import logger


def send_metadata_event(event_url, user_id, event, res):
    timestamp = str(int(time.time()))
    signature = generate_hmac_signature(timestamp)

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY,
        "X-TIMESTAMP": timestamp,
        "X-SIGNATURE": signature,
    }

    logger.info(f"UserId: {user_id} Event: {event}")

    try:
        response = httpx.post(event_url, headers=headers, json={
            "event": event,
            "userId": user_id,
            "results": res
        }, timeout=30)

        print(f"Sent event: {event}")
        response.raise_for_status()
    except httpx.RequestError as exc:
        print(f"Failed to send progress update: {exc}")
    except httpx.HTTPStatusError as exc:
        print(f"Server returned an error: {exc.response.status_code} - {exc.response.text}")
    except httpx.ReadTimeout:
        print("The request timed out while waiting for the server to send data.")
