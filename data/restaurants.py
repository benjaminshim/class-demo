"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import re

import data.db_connect as dbc
import data.users as usrs


BIG_NUM = 1_000_000_000_000_000_000_000_000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

DESCRIPTION = 'description'
ADDRESS = 'address'
CITY = 'city'
STATE = 'state'
ZIP_CODE = 'zip_code'


TEST_RESTAURANT_NAME = 'Test Restaurant'
TEST_RESTAURANT_DESCRIPTION = "A wonderful place for testing."
TEST_OWNER_ID = 100000000000000000000000

NAME = 'name'
RESTAURANT_COLLECT = 'restaurants'


TEST_RESTAURANT_FLDS = {
    TEST_RESTAURANT_NAME: 'Test Name',
    TEST_RESTAURANT_DESCRIPTION: 0,
    TEST_OWNER_ID: 0,
}


def extract_id(s):
    match = re.search(r"ObjectId\('([a-f0-9]{24})'\)", s)
    if match:
        return match.group(1)
    return None

def get_restuarants() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, RESTAURANT_COLLECT)


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def add_restaurant(name: str, description: str, address: str, city: str, state: str, zip_code: str) -> str:
    restaurants = {}
    if exists(address, city, state, zip_code):
        raise ValueError(f'A restaurant with this address already exists.')
    
    fields = {
        'name': name,
        'address': address,
        'city': city,
        'state': state,
        'zip code': zip_code,
    }

    for field, value in fields.items():
        if not value:
            raise ValueError(f'Restaurant {field} may not be blank.')
    
    restaurants[NAME] = name
    restaurants[DESCRIPTION] = description
    restaurants[ADDRESS] = address
    restaurants[CITY] = city
    restaurants[STATE] = state
    restaurants[ZIP_CODE]= zip_code

    dbc.connect_db()
    _id = dbc.insert_one(RESTAURANT_COLLECT, restaurants)
    return extract_id(str(_id))


def update_rating(name: str, rating: int) -> bool:
    if not exists(name):
        raise ValueError(f'Update failure: {name} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(RESTAURANT_COLLECT, {NAME: name},
                              {RATING: rating})


def del_restaurant(name: str):
    if exists(name):
        return dbc.del_one(RESTAURANT_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def exists(address: str, city: str, state: str, zip_code: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT, {ADDRESS: address, CITY: city, STATE: state, ZIP_CODE: zip_code})