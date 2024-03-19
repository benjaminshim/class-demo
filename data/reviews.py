import random
"""
This module interfaces to our user data
"""

import data.db_connect as dbc


BIG_NUM = 10000000000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

REVIEW_SENTENCE = 'Review'
RATING = "rating"
USER_ID = "USER_ID"
RESTAURANT_ID = "RESTAURANT_ID"

MIN_CUST_NAME_LEN = 1
REVIEW_COLLECT = 'reviews'


def _get_test_rvw():
    rvw = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return rvw + str(rand_part)


def _get_test_id():
    return str(random.randint(0, BIG_NUM))


def get_test_review():
    test_rvw = {}
    test_rvw[REVIEW_SENTENCE] = _get_test_rvw()
    test_rvw[USER_ID] = _get_test_id()
    test_rvw[RESTAURANT_ID] = _get_test_id()
    test_rvw[RATING] = _get_test_id()
    return test_rvw


def get_reviews() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(REVIEW_SENTENCE, REVIEW_COLLECT)


def exists(user: int, rstr: int) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(REVIEW_COLLECT, {USER_ID: user, RESTAURANT_ID: rstr})


def add_review(user_id: int, rest_id: int, review_str: str,
               rating: int) -> bool:
    reviews_in = {}
    if id in reviews_in:
        raise ValueError(f'Duplicate user id: {id=}')
    if not id:
        raise ValueError('Users are not allowed to be entered without ids')
    reviews_in[USER_ID] = user_id
    reviews_in[RESTAURANT_ID] = rest_id
    reviews_in[REVIEW_SENTENCE] = review_str
    reviews_in[RATING] = rating

    dbc.connect_db()
    if not exists(user_id, rest_id):
        _id = dbc.insert_one(REVIEW_COLLECT, reviews_in)
    else:
        raise ValueError('User has already reviewed this restaurant')
    return _id is not None


def update_review(user_id: int, rest_id: int,
                  review_str: str, rating: int) -> bool:
    if not exists(user_id, rest_id):
        raise ValueError('Update failure: review not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(REVIEW_COLLECT,
                              {USER_ID: user_id, RESTAURANT_ID: rest_id},
                              {RATING: rating, REVIEW_SENTENCE: review_str})
