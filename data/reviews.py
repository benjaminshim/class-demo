import random
"""
This module interfaces to our user data
"""

import data.db_connect as dbc
import data.reviews as rvws


BIG_NUM = 10000000000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

RESTAURANT_NAME = 'Restaurant Name'
REVIEW_SENTENCE = 'Review'

MIN_CUST_NAME_LEN = 1
REVIEW_COLLECT = 'reviews'


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def _get_test_rvw():
    rvw = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return rvw + str(rand_part)


def get_test_review():
    test_rvw = {}
    test_rvw[RESTAURANT_NAME] = _get_test_name()
    test_rvw[REVIEW_SENTENCE] = _get_test_rvw()
    return test_rvw


def get_reviews() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(REVIEW_SENTENCE, REVIEW_COLLECT)


def add_review(name: str, review_str: str) -> bool:
    reviews_in = {}
    if id in reviews_in:
        raise ValueError(f'Duplicate user id: {id=}')
    if not id:
        raise ValueError('Users are not allowed to be entered without ids')
    reviews_in[RESTAURANT_NAME] = name
    reviews_in[REVIEW_SENTENCE] = review_str
    dbc.connect_db()
    _id = dbc.insert_one(rvws.REVIEW_COLLECT, reviews_in)
    return _id is not None
