import json
from typing import Dict

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from ninja.errors import HttpError


def get_session_from_redis(request: HttpRequest) -> Dict:
    """Retrieves user session data from Redis cache."""

    session_cookie = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
    if not session_cookie:
        raise HttpError(500, "Internal Server Error: No session cookie found")

    redis_sessions = cache.get(session_cookie, '{}')

    try:
        session_data = json.loads(redis_sessions)
    except json.JSONDecodeError as e:
        raise HttpError(
            500, "Internal Server Error: Failed to decode session data"
        ) from e

    return session_data
