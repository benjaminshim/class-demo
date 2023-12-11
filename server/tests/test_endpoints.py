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


@pytest.fixture(scope='function')
def temp_restaurant():
    name = rst._get_test_name()
    ret = rst.add_restaurant(name, 0)
    yield name
    if rst.exists(name):
        rst.del_restaurant(name)


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_list_restaurants():
    resp = TEST_CLIENT.get(ep.RESTAURANTS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)

def test_get_restuarants():
    restaurants = rst.get_restuarants()
    assert isinstance(restaurants, dict)


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


@patch('data.db.add_restaurant', return_value=None)
def test_restaurant_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_restaurant.
    """
    resp = TEST_CLIENT.post(ep.RESTAURANTS_EP, json=rst.get_test_restaurant())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.db.del_restaurant', autospec=True)
def test_del_restaurant(mock_add):
    """
    Testing we do the right thing with a call to del_restaurant that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANTS_EP}/AnyName')
    assert resp.status_code == OK


@patch('data.db.del_restaurant', side_effect=ValueError(), autospec=True)
def test_del_restaurant_not_there(mock_add):
    """
    Testing we do the right thing with a value error from del_restaurant.
    """
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANTS_EP}/AnyName')
    assert resp.status_code == OK