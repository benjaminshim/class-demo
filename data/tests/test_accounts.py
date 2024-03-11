import server.endpoints as ep
import data.accounts as accs
from http.client import (
    NOT_ACCEPTABLE,
    OK,
    SERVICE_UNAVAILABLE,
)
from unittest.mock import patch


TEST_CLIENT = ep.app.test_client()


def test_get_account():
    account = accs.get_accounts()
    assert isinstance(account, dict)


@patch('data.accounts.add_account', return_value=accs.MOCK_ID, autospec=True)
def test_account_add(mock_add):
    resp = TEST_CLIENT.post(ep.ACCOUNTS_EP, json=accs.get_test_account())
    assert resp.status_code == OK


@patch('data.accounts.add_account', side_effect=ValueError(), autospec=True)
def test_account_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_account.
    """
    resp = TEST_CLIENT.post(ep.ACCOUNTS_EP, json=accs.get_test_account())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.accounts.add_account', return_value=None)
def test_account_add_accs_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_account.
    """
    resp = TEST_CLIENT.post(ep.ACCOUNTS_EP, json=accs.get_test_account())
    assert resp.status_code == SERVICE_UNAVAILABLE
