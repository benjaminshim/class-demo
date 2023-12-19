import random
"""
This module interfaces to our user data
"""

import data.db_connect as dbc
import data.accounts as accs


BIG_NUM = 10000000000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

ACCOUNT_SENTENCE = 'Account'
NAME = 'Name'
PASS = 'Password'

MIN_CUST_NAME_LEN = 1
ACCOUNTS_COLLECT = 'accounts'


def _get_test_acc():
    acc = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return acc + str(rand_part)


def get_test_account():
    test_acc = {}
    test_acc[ACCOUNT_SENTENCE] = _get_test_acc()
    return test_acc


def get_accounts() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(ACCOUNT_SENTENCE, ACCOUNTS_COLLECT)


def add_account(account_str: str) -> bool:
    accounts_in = {}
    if id in accounts_in:
        raise ValueError(f'Duplicate user id: {id=}')
    if not id:
        raise ValueError('Users are not allowed to be entered without ids')
    accounts_in[ACCOUNT_SENTENCE] = account_str
    dbc.connect_db()
    _id = dbc.insert_one(accs.ACCOUNTS_COLLECT, accounts_in)
    return _id is not None
