# -*- coding: utf-8 -*-
"""Phone tests."""
import json

from flask import url_for

from evolux_solution.currency.models import Currency
from evolux_solution.phone.models import Phone

# =================================================================
# Test GET method (query list)
# =================================================================


def test_phone_list(client, admin_headers):
    """Test get list of phone records."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    phone = Phone(
        value="+55 84 91234-4321",
        monthy_price="0.03",
        setup_price="3.40",
        currency_id="US",
    )
    phone.save()

    response = client.get(
        url_for("phone.phones"),
        headers=admin_headers,
    )
    expected_result = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": "1",
                "value": "+55 84 91234-4321",
                "monthyPrice": "0.03",
                "setupPrice": "3.40",
                "currency": "US",
            }
        ],
    }
    assert response.json == expected_result
    assert response.status_code == 200


def test_paginate_phone_list(client, admin_headers):
    """Test get paginated list of phone records."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    for i in range(11):
        phone = Phone(
            value=f"+55 84 91234-432{i}",
            monthy_price="0.03",
            setup_price="3.40",
            currency_id="US",
        )
        phone.save()

    response = client.get(
        url_for("phone.phones", page=2),
        headers=admin_headers,
    )
    expected_result = {
        "count": 11,
        "next": None,
        "previous": "http://localhost/api/phones/?page=1",
        "results": [
            {
                "id": "11",
                "value": "+55 84 91234-43210",
                "monthyPrice": "0.03",
                "setupPrice": "3.40",
                "currency": "US",
            }
        ],
    }
    assert response.json == expected_result
    assert response.status_code == 200


def test_invalid_paginate_phone_list(client, admin_headers):
    """Test invalid phone paginated value."""
    response = client.get(
        url_for("phone.phones", page=20),
        headers=admin_headers,
    )
    expected_result = {"count": 0, "next": None, "previous": None, "results": []}
    assert response.json == expected_result
    assert response.status_code == 200


# =================================================================
# Test GET method (query id)
# =================================================================


def test_fetch_phone_record(client, admin_headers):
    """Test get phone record by id."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    phone = Phone(
        value="+55 84 91234-4321",
        monthy_price="0.03",
        setup_price="3.40",
        currency_id="US",
    )
    phone.save()

    response = client.get(
        url_for("phone.phones", phone_id=1),
        headers=admin_headers,
    )
    expected_result = {
        "id": "1",
        "value": "+55 84 91234-4321",
        "monthyPrice": "0.03",
        "setupPrice": "3.40",
        "currency": "US",
    }
    assert response.json == expected_result


def test_fetch_invalid_phone_id(client, admin_headers):
    """Test get phone record with invalid id."""
    response = client.get(
        url_for("phone.phones", phone_id=1),
        headers=admin_headers,
    )
    expected_result = {
        "message": "Phone not found.",
    }
    assert response.json == expected_result
    assert response.status_code == 400


# =================================================================
# Test POST method
# =================================================================


def test_create_phone_record(client, admin_headers):
    """Teste create new phone record."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.post(
        url_for("phone.phones"),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "+55 84 91234-4321",
                "monthyPrice": "0.03",
                "setupPrice": "3.40",
                "currency": "US",
            }
        ),
    )
    expected_result = {
        "id": "1",
        "value": "+55 84 91234-4321",
        "monthyPrice": "0.03",
        "setupPrice": "3.40",
        "currency": "US",
    }
    assert response.json == expected_result
    assert response.status_code == 201

    phones = Phone.query.filter_by(
        id=1,
        value="+55 84 91234-4321",
        monthy_price="0.03",
        setup_price="3.40",
        currency_id="US",
    )
    assert phones.count() == 1


def test_create_duplicate_phone(client, admin_headers):
    """Teste create duplicate phone value."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    phone = Phone(
        value="+55 84 91234-4321",
        monthy_price="0.03",
        setup_price="3.40",
        currency_id="US",
    )
    phone.save()

    response = client.post(
        url_for("phone.phones"),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "+55 84 91234-4321",
                "monthyPrice": "0.03",
                "setupPrice": "3.40",
                "currency": "US",
            }
        ),
    )
    expected_result = {
        "errors": {"value": ["There is already a phone with this value."]}
    }
    assert response.json == expected_result
    assert response.status_code == 400


def test_create_invalid_phone(client, admin_headers):
    """Teste create phone with value."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.post(
        url_for("phone.phones"),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "123",
                "monthyPrice": "0.03",
                "setupPrice": "3.40",
                "currency": "US",
            }
        ),
    )
    expected_result = {
        "errors": {"value": ["Please, enter with a valid phone number."]}
    }
    assert response.json == expected_result
    assert response.status_code == 400


def test_create_negative_phone_monthly_price(client, admin_headers):
    """Teste create phone with negative monthy price."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.post(
        url_for("phone.phones"),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "+55 84 91234-4321",
                "monthyPrice": "-0.03",
                "setupPrice": "3.40",
                "currency": "US",
            }
        ),
    )
    expected_result = {"errors": {"monthyPrice": ["Value must be greater than 0."]}}
    assert response.json == expected_result
    assert response.status_code == 400


def test_create_negative_phone_setup_price(client, admin_headers):
    """Teste create phone with negative setup price."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    response = client.post(
        url_for("phone.phones"),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "+55 84 91234-4321",
                "monthyPrice": "0.03",
                "setupPrice": "-3.40",
                "currency": "US",
            }
        ),
    )
    expected_result = {"errors": {"setupPrice": ["Value must be greater than 0."]}}
    assert response.json == expected_result
    assert response.status_code == 400


def test_create_empty_currency_phone(client, admin_headers):
    """Teste create phone with invalid currency."""
    response = client.post(
        url_for("phone.phones"),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "+55 84 91234-4321",
                "monthyPrice": "0.03",
                "setupPrice": "3.40",
                "currency": "US",
            }
        ),
    )
    expected_result = {"errors": {"currency": ["There is no currency with code."]}}
    assert response.json == expected_result
    assert response.status_code == 400


# =================================================================
# Test PUT method
# =================================================================


def test_update_phone(client, admin_headers):
    """Teste update phone record."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    currency = Currency(code="€", name="Euro")
    currency.save()

    phone = Phone(
        value="+55 84 91234-4321",
        monthy_price="0.02",
        setup_price="4.20",
        currency_id="US",
    )
    phone.save()

    response = client.put(
        url_for("phone.phones", phone_id=1),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "+55 84 91234-4322",
                "monthyPrice": "0.04",
                "setupPrice": "4.40",
                "currency": "€",
            }
        ),
    )
    expected_result = {
        "id": "1",
        "value": "+55 84 91234-4322",
        "monthyPrice": "0.04",
        "setupPrice": "4.40",
        "currency": "€",
    }
    assert response.json == expected_result
    assert response.status_code == 200


def test_update_negative_phone_prices(client, admin_headers):
    """Teste update phone with negative prices."""
    dollar_currency = Currency(code="US", name="Dollar")
    dollar_currency.save()

    phone = Phone(
        value="+55 84 91234-4321",
        monthy_price="0.02",
        setup_price="4.20",
        currency_id="US",
    )
    phone.save()

    response = client.put(
        url_for("phone.phones", phone_id=1),
        headers=admin_headers,
        data=json.dumps(
            {
                "value": "+55 84 91234-4322",
                "monthyPrice": "-0.04",
                "setupPrice": "-4.40",
                "currency": "US",
            }
        ),
    )
    expected_result = {
        "errors": {
            "setupPrice": ["Value must be greater than 0."],
            "monthyPrice": ["Value must be greater than 0."],
        }
    }
    assert response.json == expected_result
    assert response.status_code == 400


# =================================================================
# Test DELETE method
# =================================================================


def test_delete_phone_record(client, admin_headers):
    """Teste delete phone record."""
    currency = Currency(code="US", name="Dollar")
    currency.save()

    phone = Phone(
        value="+55 84 91234-4322",
        monthy_price="0.04",
        setup_price="4.40",
        currency_id="US",
    )
    phone.save()

    response = client.delete(
        url_for("phone.phones", phone_id=1),
        headers=admin_headers,
    )
    expected_result = {
        "message": "Phone deleted.",
    }
    assert response.json == expected_result
    assert response.status_code == 200
    assert Phone.query.filter_by(id=1).count() == 0


def test_delete_invalid_phone(client, admin_headers):
    """Teste delete phone which does not exist."""
    response = client.delete(
        url_for("phone.phones", phone_id=1),
        headers=admin_headers,
    )
    expected_result = {
        "message": "Phone not found.",
    }
    assert response.json == expected_result
    assert response.status_code == 400
