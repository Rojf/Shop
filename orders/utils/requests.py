import requests
import json
from typing import Optional, Dict, Union

from django.http import HttpRequest
from django.conf import settings


def make_request_with_session(
    session:    requests.Session,
    payload:    Optional[dict] = None,
    headers:    Optional[dict] = None,
    method:     str = "GET",
    url:        str = ""
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
        headers=headers
    )

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("The response is not correct JSON.")
        data = dict()

    return response.status_code, data


def make_request_with_session_cookie(
    request: HttpRequest,
    url: str,
    **kwargs: dict
) -> Union[Dict, None]:
    session_cookie = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    headers = kwargs.get('headers', {})

    if session_cookie:
        if not headers.get('cookie'):
            headers['cookie'] = f'{settings.SESSION_COOKIE_NAME}={session_cookie}'
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
    return None


def make_request(
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

    try:
        response = requests.request(
            method=method,
            url=url,
            data=json.dumps(payload),
            headers=headers
        )

        #print(f"Response status: {response.status}, reason: {response.reason}")
        data = response.json()
        #print(f"Response data: {data}")
        
        return response.status_code, data
        
    except json.JSONDecodeError:
        print("The response is not correct JSON.")
        return dict()
    except Exception as e:
        print("Error occurred during API call:", e)
        return  dict()

