import data.customers as cstmrs

def test_get_customers():
  costumers = cstmrs.get_customer()
  assert isinstance(costumers, dict)
  assert len(costumers) > 0 # at least one user
  for key in costumers:
    assert isinstance(key, str)
    assert len(key) >= cstmrs.MIN_CUST_NAME_LEN
    username = costumers(key)
    assert isinstance(costumers, dict)
    assert len(username) > 0
