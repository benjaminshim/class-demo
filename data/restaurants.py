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


def get_restaurants() -> dict:
    # dbc.connect_db()
    # return dbc.fetch_all_as_dict(NAME, RESTAURANT_COLLECT)
    dbc.connect_db()
    try:
        restaurants_dict = dbc.fetch_all_as_dict(NAME, RESTAURANT_COLLECT)
        return restaurants_dict
    except Exception as e:
        print(f"Error fetching restaurants: {e}")
        return {}


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


# def add_restaurant(name: str, rating: int) -> bool:
def add_restaurant(name: str, restaurant_type: str, description: str,
                   owner_id: str, state: str, city: str,
                   address: str, zip_code: str) -> bool:
    # restaurants = {}
    # if exists(name):
    #     raise ValueError(f'Duplicate restaurant name: {name=}')
    # if not name:
    #     raise ValueError('Restaurant name may not be blank')
    # restaurants[NAME] = name
    # restaurants[RATING] = rating
    # dbc.connect_db()
    # _id = dbc.insert_one(RESTAURANT_COLLECT, restaurants)
    # # restaurants[name] = {RATING: rating}
    # return _id is not None

    # Check using both name and owner or just owner
    if exists(name):
        raise ValueError(f'Duplicate restaurant name: {name}')
    if not name:
        raise ValueError('Restaurant name may not be blank')

    search_id = _gen_id()

    restaurant_document = {
        "search_id": search_id,
        "name": name,
        "restaurant_type": restaurant_type,
        "description": description,
        "owner_id": owner_id,
        "state": state,
        "city": city,
        "address": address,
        "zip_code": zip_code,
        # rating
    }

    dbc.connect_db()
    _id = dbc.insert_one(RESTAURANT_COLLECT, restaurant_document)
    if _id is not None:
        return search_id
    else:
        return None


def get_restaurant_by_search_id(search_id: str) -> dict:
    """
    Fetch a single restaurant by its search_id.

    :param search_id: The unique search identifier for the restaurant.
    :return: The restaurant information as a dictionary if found,
             otherwise None.
    """
    dbc.connect_db()
    try:
        restaurant = dbc.fetch_one(
            RESTAURANT_COLLECT,
            {"search_id": search_id}
        )
        return restaurant
    except Exception as e:
        print(f"Error fetching restaurant by search_id {search_id}: {e}")
        return None


def update_restaurant(search_id: str, update_data: dict) -> bool:
    """
    Update a restaurant's information based on its search_id.

    :param search_id: The unique search identifier for the restaurant.
    :param update_data: A dictionary containing the fields to be updated.
    :return: True if the update was successful, False otherwise.
    """
    dbc.connect_db()
    try:
        existing_restaurant = get_restaurant_by_search_id(search_id)
        if not existing_restaurant:
            return False

        update_result = dbc.update_one(
            RESTAURANT_COLLECT,
            {"search_id": search_id},
            update_data
        )

        return update_result
    except Exception as e:
        print(f"Error updating restaurant with search_id {search_id}: {e}")
        return False


def del_restaurant(name: str):
    if exists(name):
        return dbc.del_one(RESTAURANT_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(RESTAURANT_COLLECT, {NAME: name})


def update_rating(name: str, rating: int) -> bool:
    if not exists(name):
        raise ValueError(f'Update failure: {name} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(RESTAURANT_COLLECT, {NAME: name},
                              {RATING: rating})
