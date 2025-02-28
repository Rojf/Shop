from .celery import app as celery_app  # pylint: disable=W0406,E0401

__all__ = ['celery_app']
