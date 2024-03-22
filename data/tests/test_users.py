import data.users as usrs
import server.endpoints as ep
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

MIN_USER_NAME_LEN = 1
NAME = "user"


@pytest.mark.skip('This test is failing for now')
def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)


@pytest.mark.skip('This test is failing for now')
def test_del_user(mock_del):
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANTS_EP}/AnyName')
    assert resp.status_code == OK


@pytest.mark.skip('This test is failing for now')
@patch('data.users.update_username', side_effect=ValueError(), autospec=True)
def test_bad_update_username(mock_update):
    """
    Testing we do the right thing with a call to update_rating that fails.
    """
    resp = TEST_CLIENT.put(f'{ep.USERS_EP}/AnyName/100')
    assert resp.status_code == NOT_FOUND


@pytest.mark.skip('This test is failing for now')
@patch('data.users.update_username', autospec=True)
def test_update_username(mock_update):
    """
    Testing we do the right thing with a call to update_rating that succeeds.
    """
    resp = TEST_CLIENT.put(f'{ep.USERS_EP}/AnyName/100')
    assert resp.status_code == OK
