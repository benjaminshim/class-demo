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
PASSWORD = 0
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


def exists(user_id: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USER_ID, {USER_ID: user_id})


def add_user(id: int, name: str, pw: int) -> bool:
    users = {}
    if id in users:
        raise ValueError(f'Duplicate user id: {id=}')
    if not id:
        raise ValueError('Users are not allowed to be entered without ids')
    users[USER_ID] = _gen_id()
    users[USER_NAME] = name
    users[PASSWORD] = pw
    dbc.connect_db()
    _id = dbc.insert_one(usrs.USERS_COLLECT, users)
    return _id is not None


def del_user(id: int):
    if exists(id):
        return dbc.del_one(USERS_COLLECT, {USER_ID: id})
    else:
        raise ValueError(f'Delete failure: {NAME} is not in users.')


def update_username(user_id: int, new_username: str) -> bool:
    if not exists(id):
        raise ValueError(f'Update failure: {user_id} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(USERS_COLLECT, {USER_ID: user_id},
                              {USER_NAME: new_username})
