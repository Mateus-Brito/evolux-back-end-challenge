# -*- coding: utf-8 -*-
"""User tests."""
import json
from unittest import TestCase

import pytest
from flask import url_for

from evolux_solution.user.models import User


@pytest.mark.usefixtures("db")
class TestSignup:
    """User signup tests."""

    def test_fail_to_update_dump_data(self, client):
        """Test fill dump fields on signup."""
        payload = json.dumps(
            {
                "id": "123",
                "username": "example",
                "email": "example@example.com",
                "password": "examplepassword",
                "active": False,
            }
        )
        response = client.post(
            url_for("user.register_user"),
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        expected_result = {
            "id": "1",
            "username": "example",
            "email": "example@example.com",
        }
        TestCase().assertDictEqual(response.json, expected_result)
        assert User.query.filter_by(id=1).first().active is True

    def test_duplicate_usernames(self, client):
        """Test register duplicate usernames."""
        user = User(username="example", email="example@example.com")
        user.save()

        payload = json.dumps(
            {
                "username": "example",
                "email": "example2@example.com",
                "password": "examplepassword",
            }
        )
        response = client.post(
            url_for("user.register_user"),
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        expected_result = {
            "errors": {"username": ["There is already a user with this username"]}
        }
        TestCase().assertDictEqual(response.json, expected_result)

    def test_duplicate_emails(self, client):
        """Test register duplicate emails."""
        user = User(username="example", email="example@example.com")
        user.save()

        payload = json.dumps(
            {
                "username": "example2",
                "email": "example@example.com",
                "password": "examplepassword",
            }
        )
        response = client.post(
            url_for("user.register_user"),
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        expected_result = {
            "errors": {"email": ["There is already a user with this email"]}
        }
        TestCase().assertDictEqual(response.json, expected_result)

    def test_successful_signup(self, client):
        """Test create new user."""
        payload = json.dumps(
            {
                "username": "example",
                "email": "example@example.com",
                "password": "examplepassword",
            }
        )
        response = client.post(
            url_for("user.register_user"),
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        expected_result = {
            "id": "1",
            "username": "example",
            "email": "example@example.com",
        }
        TestCase().assertDictEqual(response.json, expected_result)
        assert response.status_code == 201

    def test_user_repr(self):
        """Check __repr__ output for User."""
        user = User(username="foo", email="foo@bar.com")
        assert user.__repr__() == "<User('foo')>"


def test_get_self_user(client, admin_headers):
    """Test get authenticed user data."""
    response = client.get(
        url_for("user.get_current_user"),
        headers=admin_headers,
    )
    expected_result = {
        "id": "1",
        "username": "admin",
        "email": "admin@admin.com",
    }
    assert response.json == expected_result
