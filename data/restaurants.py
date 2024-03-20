"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import re

import data.db_connect as dbc
from bson import ObjectId


BIG_NUM = 1_000_000_000_000_000_000_000_000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

RESTAURANT_TYPE = 'restaurant_type'
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


def add_restaurant(name: str, restaurant_type: str, description: str, address: str, city: str, state: str, zip_code: str) -> str:
    restaurants = {}
    if exists(address, city, state, zip_code):
        raise ValueError(f'A restaurant with this address already exists.')
    
    fields = {
        'name': name,
        'restaurant_type': restaurant_type,
        'description': description,
        'address': address,
        'city': city,
        'state': state,
        'zip_code': zip_code,
    }

    for field, value in fields.items():
        if not value:
            raise ValueError(f'Restaurant {field} may not be blank.')
    
    restaurants[NAME] = name
    restaurants[RESTAURANT_TYPE] = restaurant_type
    restaurants[DESCRIPTION] = description
    restaurants[ADDRESS] = address
    restaurants[CITY] = city
    restaurants[STATE] = state
    restaurants[ZIP_CODE]= zip_code

    dbc.connect_db()
    _id = dbc.insert_one(RESTAURANT_COLLECT, restaurants)
    return extract_id(str(_id))


def update_restaurant(object_id: str, name: str, restaurant_type: str, description: str, address: str, city: str, state: str, zip_code: str) -> bool:
    if not id_exists(object_id):
        raise ValueError(f'This ID does not belong to a valid restaurant.')
    else:
        dbc.connect_db()
        return dbc.update_doc(RESTAURANT_COLLECT, {"_id": ObjectId(object_id)},
                              {NAME: name, RESTAURANT_TYPE: restaurant_type, DESCRIPTION: description, ADDRESS: address, CITY: city, STATE: state, ZIP_CODE: zip_code})


def del_restaurant(object_id: str):
    if not id_exists(object_id):
        raise ValueError(f'This ID does not belong to a valid restaurant.')
    else:
        dbc.connect_db()
        return dbc.del_one(RESTAURANT_COLLECT, {"_id": ObjectId(object_id)})


def exists(address: str, city: str, state: str, zip_code: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT, {ADDRESS: address, CITY: city, STATE: state, ZIP_CODE: zip_code})


def id_exists(object_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT, {"_id": ObjectId(object_id)})


def get_restaurant_by_id(object_id: str):
    """
    Fetches a restaurant from the database using its unique Object ID.
    
    :param object_id: The unique identifier for the restaurant.
    :return: The restaurant document if found, else None.
    """
    dbc.connect_db()
    restaurant = dbc.fetch_one(RESTAURANT_COLLECT, {"_id": ObjectId(object_id)})
    return restaurant