import random
"""
This module interfaces to our user data
"""

import data.db_connect as dbc
import re

from bson import ObjectId

BIG_NUM = 1_000_000_000_000_000_000_000_000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN


# NAME = 'name'
# PASSWORD = 0
# USER_NAME = "User"
# USER_ID = "_id"
# USERNAME = 'User'

USER_ID = '_id'
FIRST_NAME = 'first name'
LAST_NAME = 'last name'
EMAIL = 'email'
PASSWORD = 'password'
RESTAURANT_IDS = 'restaurant ids'

MIN_USER_NAME_LEN = 1
USERS_COLLECT = 'users'

NAME = 'not'
USER_NAME = 'not'

# def get_users() -> dict:
#     dbc.connect_db()
#     return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(EMAIL, USERS_COLLECT)


def extract_id(s):
    match = re.search(r"ObjectId\('([a-f0-9]{24})'\)", s)
    if match:
        return match.group(1)
    return None


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def exists(email: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {EMAIL: email})


def id_exists(user_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {USER_ID: ObjectId(user_id)})


def add_user(first_name: str, last_name: str,
             email: str, password: str) -> str:
    users = {}
    # if exists(email):
    #     pass

    fields = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
    }

    for field, value in fields.items():
        if not value:
            raise ValueError(f'Restaurant {field} may not be blank')

    users[FIRST_NAME] = first_name
    users[LAST_NAME] = last_name
    users[EMAIL] = email
    users[PASSWORD] = password
    users[RESTAURANT_IDS] = []

    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, users)
    return extract_id(str(_id))


def del_user(user_id: str):
    if not id_exists(user_id):
        raise ValueError(f'Delete failure: {user_id} not in database.')
    else:
        dbc.connect_db()
        return dbc.del_one(USERS_COLLECT, {USER_ID: ObjectId(user_id)})


def update_email(user_id: str, new_email: str) -> bool:
    if not id_exists(user_id):
        raise ValueError(f'Update failure: {user_id} not in database.')
    dbc.connect_db()
    return dbc.update_doc(USERS_COLLECT, {"_id": ObjectId(user_id)},
                          {EMAIL: new_email})
