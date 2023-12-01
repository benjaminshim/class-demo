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


# def get_old_users():
#     users = {
#         "Jason": {
#             USERNAME: 'jl1002',
#         },
#         "Natalie": {
#             USERNAME: 'nw2003',
#         },
#         "Kevin": {
#             USERNAME: 'ks3004',
#         },
#         "Chris": {
#             USERNAME: 'ch4005',
#         },
#     }
#     return users
