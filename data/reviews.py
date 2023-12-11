# Import all lines from 2-30
import random
"""
This module interfaces to our user data
"""

import data.db_connect as dbc
import data.reviews as rvws         # Change this


BIG_NUM = 10000000000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

REVIEW_SENTENCE = 'Review'          # REVIEW_SENTENCE is what people are going to see
# Maybe put...
# NAME = 'Name'
# PASS = 'Password'

MIN_CUST_NAME_LEN = 1
REVIEW_COLLECT = 'reviews'      # Important bc this is how the database knows to create a new collection
                                # Must have the format ''_COLLECT
                                # So maybe put something like ACCOUNTS_COLLECT = 'accounts'


# Ask Andy lol
def _get_test_rvw(): # this would be _get_test_acc
    rvw = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return rvw + str(rand_part)


def get_test_review():
    test_rvw = {}
    test_rvw[REVIEW_SENTENCE] = _get_test_rvw()     # REVIEW_SENTENCE is what people are going to see
    return test_rvw


def get_reviews() -> dict: 
    dbc.connect_db()
    return dbc.fetch_all_as_dict(REVIEW_SENTENCE, REVIEW_COLLECT) # return (NAME, PASSWORD, COLLECTION)


def add_review(review_str: str) -> bool:    # pass name and password parameters (both strings)
    reviews_in = {}
    if id in reviews_in:
        raise ValueError(f'Duplicate user id: {id=}')
    if not id:
        raise ValueError('Users are not allowed to be entered without ids')
    reviews_in[REVIEW_SENTENCE] = review_str
    dbc.connect_db()
    _id = dbc.insert_one(rvws.REVIEW_COLLECT, reviews_in)
    return _id is not None
