"""
This module interfaces to our customer data
"""

USERNAME = 'Username'
MIN_CUST_NAME_LEN = 2


def get_customer():
    customers = {
      "Andy": {
        USERNAME: 'andy123',
      },
      "Benji": {
        USERNAME: 'benji234',
      },
      "Carolina": {
        USERNAME: 'carol345',
      },
      "Bridget": {
        USERNAME: 'bridg456',
      },
    }
    return customers
