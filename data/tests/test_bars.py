import server.endpoints as ep
import data.bars as brs
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


@patch('data.bars.add_bar', return_value=brs.MOCK_ID, autospec=True)
def test_bar_add(mock_add):
    resp = TEST_CLIENT.post(ep.BAR_EP, json=brs.get_test_bar())
    assert resp.status_code == OK


@patch('data.bars.add_bar', side_effect=ValueError(), autospec=True)
def test_bar_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_bar.
    """
    resp = TEST_CLIENT.post(ep.BAR_EP, json=brs.get_test_bar())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.bars.add_bar', return_value=None)
def test_bar_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_bar.
    """
    resp = TEST_CLIENT.post(ep.BAR_EP, json=brs.get_test_bar())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.bars.update_bar_rating', side_effect=ValueError(), autospec=True)
def test_bad_update_bar_rating(mock_update):
    """
    Testing we do the right thing with a call to update_bar_rating that fails.
    """
    resp = TEST_CLIENT.put(f'{ep.BAR_EP}/AnyName/100')
    assert resp.status_code == NOT_FOUND


@patch('data.bars.update_bar_rating', autospec=True)
def test_update_rating(mock_update):
    """
    Testing we do the right thing with a call to update_bar_rating that succeeds.
    """
    resp = TEST_CLIENT.put(f'{ep.BAR_EP}/AnyName/100')
    assert resp.status_code == OK
