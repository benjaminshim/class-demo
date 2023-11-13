import data.users as usrs

MIN_USER_NAME_LEN = 1

def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    # assert len(users) > 0
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        assert isinstance(user[usrs.LEVEL], int)