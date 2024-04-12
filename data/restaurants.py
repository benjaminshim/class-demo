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


def get_restaurants_by_state(state: str) -> list:
    """
    Fetches a list of restaurants filtered by the specified state.

    Args:
        state (str): The state to filter the restaurants by.

    Returns:
        list: A list of dictionaries representing the restaurants in the specified state.
    """
    dbc.connect_db()  # Ensure the database connection is established
    # Fetch all restaurants filtered by the state parameter
    filtered_restaurants = dbc.fetch_all_filtered(RESTAURANT_COLLECT, filt={STATE: state})
    return filtered_restaurants


def add_restaurant(name: str, restaurant_type: str, description: str,
                   address: str, city: str, state: str, zip_code: str) -> str:
    restaurants = {}
    if exists(address, city, state, zip_code):
        raise ValueError('A restaurant with this address already exists.')

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
    restaurants[ZIP_CODE] = zip_code

    dbc.connect_db()
    _id = dbc.insert_one(RESTAURANT_COLLECT, restaurants)
    return extract_id(str(_id))


def update_restaurant(restaurant_id: str, restaurant_data: dict) -> bool:
    if not id_exists(restaurant_id):
        raise ValueError('This ID does not belong to a valid restaurant.')

    if not restaurant_data:
        raise ValueError('There are no valid fields to update.')

    update_data = {}
    for key in [NAME, RESTAURANT_TYPE, DESCRIPTION,
                ADDRESS, CITY, STATE, ZIP_CODE]:
        if key in restaurant_data:
            update_data[key] = restaurant_data[key]

    dbc.connect_db()
    return dbc.update_doc(RESTAURANT_COLLECT,
                          {"_id": ObjectId(restaurant_id)}, update_data)


def del_restaurant(object_id: str):
    if not id_exists(object_id):
        raise ValueError('This ID does not belong to a valid restaurant.')
    else:
        dbc.connect_db()
        return dbc.del_one(RESTAURANT_COLLECT,
                           {"_id": ObjectId(object_id)})


def exists(address: str, city: str, state: str, zip_code: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT,
                         {ADDRESS: address, CITY: city,
                          STATE: state, ZIP_CODE: zip_code})


def id_exists(object_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT,
                         {"_id": ObjectId(object_id)})


def get_restaurant_by_id(object_id: str):
    dbc.connect_db()
    restaurant = dbc.fetch_one(RESTAURANT_COLLECT,
                               {"_id": ObjectId(object_id)})
    return restaurant


def get_restaurants_filt(state: str, city: str) -> list:
    dbc.connect_db()
    return dbc.fetch_all_filtered(RESTAURANT_COLLECT,
                                  filt={STATE: state, CITY: city})
