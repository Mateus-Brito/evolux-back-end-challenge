# -*- coding: utf-8 -*-
"""Currency tests."""
import json

from flask import url_for

from evolux_solution.currency.models import Currency

# =================================================================
# Test GET method (query list)
# =================================================================


def test_currency_list(client, admin_headers):
    """Test get list of currency records."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.get(
        url_for("currency.currencies"),
        headers=admin_headers,
    )
    expected_result = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "code": "US",
                "name": "Dollar",
            }
        ],
    }
    assert response.json == expected_result
    assert response.status_code == 200


def test_paginate_currency_list(client, admin_headers):
    """Test get paginated list of currency records."""
    for i in range(11):
        currency = Currency(code=f"US-{i}", name="Dollar")
        currency.save()

    response = client.get(
        url_for("currency.currencies", page=2),
        headers=admin_headers,
    )
    expected_result = {
        "count": 11,
        "next": None,
        "previous": "http://localhost/api/currencies/?page=1",
        "results": [
            {
                "code": "US-10",
                "name": "Dollar",
            }
        ],
    }
    assert response.json == expected_result
    assert response.status_code == 200


def test_invalid_paginate_currency_list(client, admin_headers):
    """Test invalid currency paginated value."""
    response = client.get(
        url_for("currency.currencies", page=20),
        headers=admin_headers,
    )
    expected_result = {"count": 0, "next": None, "previous": None, "results": []}
    assert response.json == expected_result
    assert response.status_code == 200


# =================================================================
# Test GET method (query id)
# =================================================================


def test_fetch_currency_insensitive_code(client, admin_headers):
    """Test currency insensitive code filter."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.get(
        url_for("currency.currencies", code="us"),
        headers=admin_headers,
    )
    expected_result = {
        "code": "US",
        "name": "Dollar",
    }
    assert response.json == expected_result


def test_fetch_invalid_currency_code(client, admin_headers):
    """Test filter with invalid currency code."""
    response = client.get(
        url_for("currency.currencies", code="us"),
        headers=admin_headers,
    )
    expected_result = {
        "message": "Currency not found",
    }
    assert response.json == expected_result
    assert response.status_code == 400


# =================================================================
# Test POST method
# =================================================================


def test_create_currency_record(client, admin_headers):
    """Teste create new currency record."""
    response = client.post(
        url_for("currency.currencies"),
        headers=admin_headers,
        data=json.dumps({"code": "€", "name": "Euro"}),
    )
    expected_result = {
        "code": "€",
        "name": "Euro",
    }
    assert response.json == expected_result
    assert response.status_code == 201
    assert Currency.query.filter_by(**expected_result).count() == 1


def test_create_empty_currency_code(client, admin_headers):
    """Teste create currency with empty code."""
    response = client.post(
        url_for("currency.currencies"),
        headers=admin_headers,
        data=json.dumps({"name": "Euro"}),
    )
    expected_result = {"errors": {"code": ["Missing data for required field."]}}
    assert response.json == expected_result
    assert response.status_code == 400


def test_create_empty_currency_name(client, admin_headers):
    """Teste create currency with empty name."""
    response = client.post(
        url_for("currency.currencies"),
        headers=admin_headers,
        data=json.dumps({"code": "US"}),
    )
    expected_result = {"errors": {"name": ["Missing data for required field."]}}
    assert response.json == expected_result
    assert response.status_code == 400


def test_create_duplicate_currency_code(client, admin_headers):
    """Teste create duplicate currency code."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.post(
        url_for("currency.currencies"),
        headers=admin_headers,
        data=json.dumps({"code": "US", "name": "Dollar"}),
    )
    expected_result = {
        "errors": {"code": ["There is already a currency with this code."]}
    }
    assert response.json == expected_result
    assert response.status_code == 400


# =================================================================
# Test PUT method
# =================================================================


def test_update_currency_name(client, admin_headers):
    """Teste update currency name."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.put(
        url_for("currency.currencies", code="us"),
        headers=admin_headers,
        data=json.dumps({"code": "US", "name": "Euro"}),
    )
    expected_result = {"code": "US", "name": "Euro"}
    assert response.json == expected_result
    assert response.status_code == 200
    assert Currency.query.filter_by(**expected_result).count() == 1


def test_update_duplicate_currency_code(client, admin_headers):
    """Teste update currency to duplicate name."""
    dollar_currency = Currency(code="US", name="Dollar")
    dollar_currency.save()

    euro_currency = Currency(code="€", name="Euro")
    euro_currency.save()

    response = client.put(
        url_for("currency.currencies", code="us"),
        headers=admin_headers,
        data=json.dumps({"code": "€", "name": "Euro"}),
    )
    expected_result = {
        "errors": {"code": ["There is already a currency with this code."]}
    }
    assert response.json == expected_result
    assert response.status_code == 400


def test_update_invalid_currency(client, admin_headers):
    """Teste update currency which does not exist."""
    response = client.put(
        url_for("currency.currencies", code="us"),
        headers=admin_headers,
        data=json.dumps({"code": "€", "name": "Euro"}),
    )
    expected_result = {
        "message": "Currency not found",
    }
    assert response.json == expected_result
    assert response.status_code == 400


# =================================================================
# Test DELETE method
# =================================================================


def test_delete_currency_record(client, admin_headers):
    """Teste delete currency record."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.delete(
        url_for("currency.currencies", code="us"),
        headers=admin_headers,
    )
    expected_result = {
        "message": "Currency deleted.",
    }
    assert response.json == expected_result
    assert response.status_code == 200
    assert Currency.query.filter_by(code="US").count() == 0


def test_delete_invalid_currency(client, admin_headers):
    """Teste delete currency which does not exist."""
    response = client.delete(
        url_for("currency.currencies", code="us"),
        headers=admin_headers,
    )
    expected_result = {
        "message": "Currency not found.",
    }
    assert response.json == expected_result
    assert response.status_code == 400


# =================================================================
# Test invalid authorization
# =================================================================


def test_unauthorized_list_currencies(client, db):
    """Teste get currencies from unauthorized access."""
    response = client.get(
        url_for("currency.currencies", code="us"),
        headers={"content-type": "application/json"},
    )
    expected_result = {
        "message": "Missing Authorization Header",
    }
    assert response.json == expected_result
    assert response.status_code == 401


def test_unauthorized_get_currency(client, db):
    """Teste get currency from unauthorized access."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.get(
        url_for("currency.currencies", code="us"),
        headers={"content-type": "application/json"},
    )
    expected_result = {
        "message": "Missing Authorization Header",
    }
    assert response.json == expected_result
    assert response.status_code == 401


def test_unauthorized_create_currency(client, db):
    """Teste create currency from unauthorized access."""
    response = client.post(
        url_for("currency.currencies"),
        headers={"content-type": "application/json"},
        data=json.dumps({"code": "€", "name": "Euro"}),
    )
    expected_result = {
        "message": "Missing Authorization Header",
    }
    assert response.json == expected_result
    assert response.status_code == 401


def test_unauthorized_update_currency(client, db):
    """Teste update currency from unauthorized access."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.put(
        url_for("currency.currencies", code="us"),
        headers={"content-type": "application/json"},
    )
    expected_result = {
        "message": "Missing Authorization Header",
    }
    assert response.json == expected_result
    assert response.status_code == 401


def test_unauthorized_delete_currency(client, db):
    """Teste delete currency from unauthorized access."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.delete(
        url_for("currency.currencies", code="us"),
        headers={"content-type": "application/json"},
    )
    expected_result = {
        "message": "Missing Authorization Header",
    }
    assert response.json == expected_result
    assert response.status_code == 401


# =================================================================
# Another tests
# =================================================================


def test_currency_repr():
    """Check __repr__ output for Currency object."""
    currency = Currency(code="US", name="US Dollar")
    assert currency.__repr__() == "<Currency('US')>"
