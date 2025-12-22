import hashlib
import hmac
import time

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.config.config import API_KEY, API_SECRET

# Define header dependencies
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)
timestamp_header = APIKeyHeader(name="X-TIMESTAMP", auto_error=True)
signature_header = APIKeyHeader(name="X-SIGNATURE", auto_error=True)

def validate_hmac_signature(
    api_key: str = Security(api_key_header),
    x_timestamp: str = Security(timestamp_header),
    x_signature: str = Security(signature_header),
):
    # Validate API Key
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # Check if the timestamp is within a valid range (e.g., 5 minutes)
    try:
        current_time = int(time.time())
        timestamp = int(x_timestamp)
        if abs(current_time - timestamp) > 300:
            raise HTTPException(status_code=403, detail="Timestamp expired")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")

    # Generate the expected HMAC signature
    payload = f"{api_key}:{x_timestamp}"
    expected_signature = hmac.new(
        API_SECRET.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()

    # Compare the received signature with the expected one
    if not hmac.compare_digest(x_signature, expected_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

def generate_hmac_signature(timestamp: str) -> str:
    payload = f"{API_KEY}:{timestamp}"
    expected_signature = hmac.new(
        API_SECRET.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()

    return expected_signature

