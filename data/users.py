"""
This module interfaces to our user data
"""

USERNAME = 'testuser1234'
MIN_CUST_NAME_LEN = 1


def get_user():
    users = {
        "Jason": {
            USERNAME: 'jl1002',
        },
        "Natalie": {
            USERNAME: 'nw2003',
        },
        "Kevin": {
            USERNAME: 'ks3004',
        },
        "Chris": {
            USERNAME: 'ch4005',
        },
    }
    return users
