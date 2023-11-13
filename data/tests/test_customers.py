import data.customers as cstmrs


def test_get_customers():
    cust = cstmrs.get_users()
    assert isinstance(cust, dict)
    assert len(cust) > 0  # at least one user!
