import json
from typing import Any, Dict, Optional, Union

import requests
from django.conf import settings
from django.http import HttpRequest
from ninja.errors import HttpError


def make_request_with_session_cookie(
    request: HttpRequest, url: str, timeout: int = 10, **kwargs: dict
) -> Union[Dict, None]:
    session_cookie = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    headers = kwargs.get('headers', {})

    if session_cookie:
        if not headers.get('cookie'):
            headers['cookie'] = f'{settings.SESSION_COOKIE_NAME}={session_cookie}'

        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            return response.json()
    return None


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
