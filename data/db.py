"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random

BIG_NUM = 10000000000000
ID_LEN = 24

RATING = 'rating'
TEST_RESTAURANT_NAME = 'Dominos'

restaurants = {
    'Papa Johns': {
        RATING: 5,
    },
    TEST_RESTAURANT_NAME: {
        RATING: 5,
    },
}

def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}

def get_restuarants() -> dict:
    return restaurants

def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id

def add_restaurant(name: str, rating: int) -> str:
    if name in restaurants:
        raise ValueError(f'Duplicate game name: {name=}')
    if not name:
        raise ValueError('Game name may not be blank')
    restaurants[name] = {RATING: rating}
    return _gen_id()

