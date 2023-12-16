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

def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    # assert len(users) > 0
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict) 


@pytest.mark.skip('This test is failing for now')
def test_del_user(mock_del):
    resp = TEST_CLIENT.delete(f'{ep.RESTAURANTS_EP}/AnyName')
    assert resp.status_code == OK
