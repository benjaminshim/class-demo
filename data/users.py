from genericpath import exists
import random
"""
This module interfaces to our user data
"""

import data.db_connect as dbc
import data.users as usrs


BIG_NUM = 10000000000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

NAME = 'name'

USER_NAME = "User"
USER_ID = "_id"

USERNAME = 'User'
MIN_CUST_NAME_LEN = 1
USERS_COLLECT = 'users'


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def add_user(name: str, id: int) -> bool:
    users = {}
    if id in users:
        raise ValueError(f'Duplicate user id: {id=}')
    if not id:
        raise ValueError('Users are not allowed to be entered without ids')
    users[USER_ID] = _gen_id()
    users[USER_NAME] = name
    dbc.connect_db()
    _id = dbc.insert_one(usrs.USERS_COLLECT, users)
    return _id is not None


def del_user(name:str): 
    if exists(name):
        dbc.del_one(USERS_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} is not in users.')
