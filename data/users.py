"""
This module interfaces to our user data
"""

import data.db_connect as dbc

USERNAME = 'User'
MIN_CUST_NAME_LEN = 1
USERS_COLLECT = 'users'


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)
