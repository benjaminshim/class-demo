"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random

import data.db_connect as dbc
import data.users as usrs


BIG_NUM = 1_000_000_000_000_000_000_000_000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

TEST_RESTAURANT_NAME = 'Test Restaurant'
TEST_RESTAURANT_DESCRIPTION = "A wonderful place for testing."
TEST_OWNER_ID = 100000000000000000000000

NAME = 'name'
DESCRIPTION = 'description'
OWNER_ID = 'owner_id'

RESTAURANT_COLLECT = 'restaurants'

TEST_RESTAURANT_FLDS = {
    TEST_RESTAURANT_NAME: 'Test Name',
    TEST_RESTAURANT_DESCRIPTION: 0,
    TEST_OWNER_ID: 0
}


restaurants = {
    'Test_Restaurant': {
        DESCRIPTION: TEST_RESTAURANT_DESCRIPTION,
        OWNER_ID: TEST_OWNER_ID,
    },
}


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


def del_restaurant(name: str):
    if exists(name):
        return dbc.del_one(RESTAURANT_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT, {NAME: name})


# def update_rating(name: str, rating: int) -> bool:
#     if not exists(name):
#         raise ValueError(f'Update failure: {name} not in database.')
#     else:
#         dbc.connect_db()
#         return dbc.update_doc(RESTAURANT_COLLECT, {NAME: name},
#                               {RATING: rating})
