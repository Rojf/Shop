import json
from typing import Any, Dict, Optional

import requests
from ninja.errors import HttpError


def make_request(
    method: str,
    url: str,
    payload: Optional[dict] = None,
    headers: Optional[dict] = None,
    timeout: int = 10,
) -> Dict[str, Any]:
    if payload is None:
        payload = {}
    if headers is None:
        headers = {"Content-Type": "application/json"}

    try:
        response = requests.request(
            method=method,
            url=url,
            json=payload,
            headers=headers,
            timeout=timeout,
        )

        response.raise_for_status()
        return response.json()

    except json.JSONDecodeError as e:
        print("Invalid JSON response")
        raise HttpError(400, "Invalid response format") from e

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
        raise HttpError(500, "External API request failed") from e

    except Exception as exc:
        print("Error occurred during API call:", exc)
        raise HttpError(500, "") from exc
