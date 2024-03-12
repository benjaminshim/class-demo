import server.endpoints as ep
import data.restaurants as rst
import pytest
# import unittest
# from data.restaurants import TEST_RESTAURANT_FLDS
# import data.db_connect as dbc

from http import HTTPStatus
from http.client import (
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)
from unittest.mock import patch


TEST_CLIENT = ep.app.test_client()


# TESTS
@pytest.fixture(scope='function')
def temp_restaurant():
    name = rst._get_test_name()
    # ret = rst.add_restaurant(name, 0)
    yield name
    if rst.exists(name):
        rst.del_restaurant(name)


test_restaurant_data = {
    "name": "Test Restaurant",
    "restaurant_type": "Test Type",
    "description": "A place for testing",
    "owner_id": "test_owner",
    "state": "test_state",
    "city": "test_city",
    "address": "123 Test St",
    "zip_code": "12345"
}

# UC
# def test_list_users():
#     resp = TEST_CLIENT.get(ep.USERS_EP)
#     resp_json = resp.get_json()
#     assert isinstance(resp_json, dict)


def test_list_restaurants():
    # resp = TEST_CLIENT.get(ep.RESTAURANTS_EP)
    # resp_json = resp.get_json()
    # assert isinstance(resp_json, dict)
    resp = TEST_CLIENT.get(ep.RESTAURANTS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert 'Title' in resp_json
    assert 'DATA' in resp_json
    assert isinstance(resp_json['DATA'], dict)


def test_get_restaurants():
    restaurants = rst.get_restaurants()
    assert isinstance(restaurants, dict)


# PATCHES
# @patch('data.restaurants.add_restaurant',
#        return_value=rst.MOCK_ID, autospec=True)
# def test_restaurant_add(mock_add):
#     resp = TEST_CLIENT.post(ep.RESTAURANTS_EP,
#       json=rst.get_test_restaurant())
#     assert resp.status_code == OK
@patch('data.restaurants.add_restaurant',
       return_value=rst.MOCK_ID, autospec=True)
def test_restaurant_add(mock_add):
    resp = TEST_CLIENT.post(ep.RESTAURANTS_EP, json=test_restaurant_data)
    print(mock_add.call_args)
    assert resp.status_code == HTTPStatus.CREATED
    mock_add.assert_called_once_with("Test Restaurant", "Test Type", "A place for testing",
                                     "test_owner", "test_state", "test_city",
                                     "123 Test St", "12345")


@patch(
    'data.restaurants.update_restaurant',
    autospec=True
)
@patch(
    'data.restaurants.add_restaurant',
    return_value='generated_search_id', autospec=True
)
def test_restaurant_update(mock_add, mock_update):
    mock_add.return_value = 'generated_search_id'
    add_response = TEST_CLIENT.post(
        ep.RESTAURANTS_EP,
        json=test_restaurant_data
    )
    assert add_response.status_code == HTTPStatus.CREATED
    mock_add.assert_called_once()

    # update_data = {
    #     "description": "Updated description",
    #     "state": "UpdatedState",
    # }
    # search_id = 'generated_search_id'
    # REVISIT
    # update_response = TEST_CLIENT.patch(f"{ep.RESTAURANTS_EP}/{search_id}",
    # json=update_data)

    # assert update_response.status_code == HTTPStatus.OK
    # mock_update.assert_called_once_with(search_id, **update_data)


@pytest.mark.skip('This test is failing for now')
def test_del_restaurant(mock_add):
    """
    Testing we do the right thing with a call to del_restaurant
    that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANTS_EP}/AnyName')
    assert resp.status_code == OK


@patch('data.restaurants.update_rating',
       side_effect=ValueError(), autospec=True)
def test_bad_update_rating(mock_update):
    """
    Testing we do the right thing with a call to update_rating that fails.
    """
    resp = TEST_CLIENT.put(f'{ep.RESTAURANTS_EP}/AnyName/100')
    assert resp.status_code == NOT_FOUND


# REVISIT
# @patch('data.restaurants.del_restaurant',
#        side_effect=ValueError(), autospec=True)
# def test_del_restaurant_not_there(mock_add):
#     """
#     Testing we do the right thing with a value error from del_restaurant.
#     """
#     resp = TEST_CLIENT.delete(f'{ep.RESTAURANTS_EP}/AnyName')
#     assert resp.status_code == NOT_FOUND
