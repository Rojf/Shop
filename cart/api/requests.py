import http.client
import requests
import json
from typing import Optional


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
        return dict()

