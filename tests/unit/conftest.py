"""Unit tests must never send real HTTP requests."""

import pytest
import requests


@pytest.fixture(autouse=True)
def block_http(monkeypatch):
    def fail_request(*args, **kwargs):
        raise AssertionError("Real HTTP requests are forbidden in unit tests")

    monkeypatch.setattr(requests.sessions.Session, "request", fail_request)
