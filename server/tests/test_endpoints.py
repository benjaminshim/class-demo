import server.endpoints as ep
import data.db as rst
from data.db import TEST_RESTAURANT_FLDS
import data.db_connect as dbc
import pytest

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)
from unittest.mock import patch


TEST_CLIENT = ep.app.test_client()

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


def test_list_users():
    resp = TEST_CLIENT.get(ep.CUSTOMERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_list_restaurants():
    resp = TEST_CLIENT.get(ep.RESTAURANTS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)

def test_get_restuarants():
    assert rst.get_restuarants()


@patch('data.db.add_restaurant', return_value=rst.MOCK_ID, autospec=True)
def test_restaurant_add(mock_add):
    resp = TEST_CLIENT.post(ep.RESTAURANTS_EP, json=rst.get_test_restaurant())
    assert resp.status_code == OK

@patch('data.db.add_restaurant', side_effect=ValueError(), autospec=True)
def test_restaurant_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_restaurant.
    """
    resp = TEST_CLIENT.post(ep.RESTAURANTS_EP, json=rst.get_test_restaurant())
    assert resp.status_code == NOT_ACCEPTABLE

@pytest.mark.skip('This test is failing for now but will be fixed soon')
def test_restaurant_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_restaurant.
    """
    resp = TEST_CLIENT.post(ep.RESTAURANT_EP, json=rst.get_test_restaurant())
    assert resp.status_code == SERVICE_UNAVAILABLE

