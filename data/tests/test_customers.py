import data.customers as cstmrs


def test_get_customer():
    customers = cstmrs.get_customer()
    assert isinstance(customers, dict)
    assert len(customers) > 0  # at least one user!
    for key in customers:
        assert isinstance(key, str)
        assert len(key) >= cstmrs.MIN_CUST_NAME_LEN
        user = customers[key]
        assert isinstance(user, dict)
        assert cstmrs.USERNAME in user
        assert isinstance(user[cstmrs.USERNAME], str)
