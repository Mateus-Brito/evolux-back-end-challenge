# -*- coding: utf-8 -*-
"""Providing fixtures for the directory."""
import json
import logging

import pytest

from evolux_solution.app import create_app
from evolux_solution.database import db as _db
from evolux_solution.user.models import User


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture()
def client(app):
    """Create client for the tests."""
    return app.test_client()


@pytest.fixture
def admin_user(db):
    """Create a user for the tests."""
    user = User(username="admin", email="admin@admin.com", password="admin")
    user.save()
    return user


@pytest.fixture
def admin_headers(admin_user, client):
    """Create headers with access token for the tests."""
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["access_token"],
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    """Create headers with refresh token for the tests."""
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["refresh_token"],
    }
