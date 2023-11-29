"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random

import data.db_connect as dbc


BIG_NUM = 10000000000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

RATING = 'rating'
TEST_RESTAURANT_NAME = 'Restaurant'

NAME = 'name'
RESTAURANT_COLLECT = 'restaurants'

TEST_RESTAURANT_FLDS = {
    TEST_RESTAURANT_NAME: 'Test name',
    RATING: 0,
}


restaurants = {
    'Papa Johns': {
        RATING: 5,
    },
    TEST_RESTAURANT_NAME: {
        RATING: 5,
    },
}


NAME = 'name'


users = {
    10000: {
        NAME: "James"
    },
    10001: {
        NAME: "Jessie"
    },
}


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_restaurant():
    test_rest = {}
    test_rest[TEST_RESTAURANT_NAME] = _get_test_name()
    test_rest[RATING] = 0
    return test_rest


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}


def get_restuarants() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, RESTAURANT_COLLECT)


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def add_restaurant(name: str, rating: int) -> bool:
    restaurants = {}
    if exists(name):
        raise ValueError(f'Duplicate restaurant name: {name=}')
    if not name:
        raise ValueError('Restaurant name may not be blank')
    restaurants[NAME] = name
    restaurants[RATING] = rating
    dbc.connect_db()
    _id = dbc.insert_one(RESTAURANT_COLLECT, restaurants)
    # restaurants[name] = {RATING: rating}
    return _id is not None


def add_user(name: str, id: int) -> bool:
    if id in users:
        raise ValueError(f'Duplicate user id: {id=}')
    if not id:
        raise ValueError('Users are not allowed to be entered without ids')
    users[id] = {NAME: name}
    dbc.connect_db()
    return _gen_id()


def del_restaurant(name: str):
    if exists(name):
        return dbc.del_one(RESTAURANT_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def del_user(id: int):
    if exists(id):
        del users[id]
    else:
        raise ValueError(f'Delete failure: {id} is not in users.')


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT, {NAME: name})
