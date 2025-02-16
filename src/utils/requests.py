import json
from typing import Dict, Optional, Union

import requests
from django.conf import settings
from django.http import HttpRequest
from ninja.errors import HttpError


def make_request_with_session(
    session: requests.Session,
    payload: Optional[dict] = None,
    headers: Optional[dict] = None,
    method: str = "GET",
    url: str = "",
):
    if payload is None:
        payload = {}

    if headers is None:
        headers = {
            "Content-Type": "application/json",
        }

    response = session.request(
        method=method,
        url=url,
        data=json.dumps(payload),
        headers=headers,
    )

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("The response is not correct JSON.")
        data = {}

    return response.status_code, data


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
    payload: Optional[dict] = None,
    headers: Optional[dict] = None,
    method: str = "GET",
    url: str = "",
    timeout: int = 10,
):
    if payload is None:
        payload = {}
    if headers is None:
        headers = {
            "Content-Type": "application/json",
        }

    try:
        response = requests.request(
            method=method,
            url=url,
            data=json.dumps(payload),
            headers=headers,
            timeout=timeout,
        )

        if response.status_code != 200:
            raise HttpError(response.status_code, f"Error from API: {response.reason}")

        # print(f"Response status: {response.status}, reason: {response.reason}")
        data = response.json()
        # print(f"Response data: {data}")

        return response.status_code, data

    except json.JSONDecodeError as exc:
        print("The response is not correct JSON.")
        raise HttpError(400, "") from exc
    except Exception as exc:
        print("Error occurred during API call:", exc)
        raise HttpError(500, "") from exc
