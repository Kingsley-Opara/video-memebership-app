import pytest
from app.users.models import User
from app import db

@pytest.fixture(scope='module')
def setUp():
    session = db.get_session()
    yield session
    q = User.objects.filter(email='test@test.com')
    if q.count() != 0:
        q.delete()
    session.shutdown()

def test_good():
    with pytest.raises(AssertionError):
        assert True is not True

def test_create_users(setUp):
    assert User.create_user(email = 'test@test.com', password= 'abcd1234')