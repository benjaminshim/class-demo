import random
import data.db_connect as dbc


BIG_NUM = 10000000000000
ID_LEN = 24
MOCK_ID = '0' * ID_LEN

MIN_BAR_NAME_LEN = 1
BAR_COLLECT = 'bars'
BAR_RATING = 'rating'
BAR = 'bar'


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_bar():
    test_rest = {}
    test_rest[BAR] = _get_test_name()
    test_rest[BAR_RATING] = 0
    return test_rest


def get_bars() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(BAR, BAR_COLLECT)


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(BAR_COLLECT, {BAR: name})


def add_bar(name: str, rating: int) -> bool:
    bars = {}
    if exists(name):
        raise ValueError(f'Duplicate bar name: {name=}')
    if not name:
        raise ValueError('bar name may not be blank')
    bars[BAR] = name
    bars[BAR_RATING] = rating
    dbc.connect_db()
    _id = dbc.insert_one(BAR_COLLECT, bars)
    return _id is not None


def update_bar_rating(name: str, rating: int) -> bool:
    if not exists(name):
        raise ValueError(f'Update failure: {name} not in database.')
    else:
        dbc.connect_db()
        return dbc.update_doc(BAR_COLLECT, {BAR: name},
                              {BAR_RATING: rating})
