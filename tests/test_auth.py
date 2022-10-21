# -*- coding: utf-8 -*-
"""Auth tests."""
from flask import url_for


def test_revoke_access_token(client, admin_headers):
    """Test revoke access token."""
    resp = client.delete(url_for("auth.revoke_access_token"), headers=admin_headers)
    assert resp.status_code == 200

    resp = client.get(url_for("user.get_current_user"), headers=admin_headers)
    assert resp.status_code == 401


def test_revoke_refresh_token(client, admin_refresh_headers):
    """Test revoke refresh token."""
    resp = client.delete(
        url_for("auth.revoke_refresh_token"), headers=admin_refresh_headers
    )
    assert resp.status_code == 200

    resp = client.post(url_for("auth.refresh"), headers=admin_refresh_headers)
    assert resp.status_code == 401
