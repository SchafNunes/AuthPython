from app.users.models import User

def test_create_user(test_client):
    user = User(username="testuser", email="testuser@gmail.com")
    user.set_password("testpassword")
    user.save()
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "testuser@gmail.com"
    assert user.check_password("testpassword")

def test_get_user_by_username(test_client):
    user = User(username="testuser", email="testuser@gmail.com")
    user.set_password("testpassword")
    user.save()
    
    fetched_user = User.get_user_by_username("testuser")
    assert fetched_user is not None
    assert fetched_user.username == "testuser"

def test_check_password(test_client):
    user = User(username="testuser", email="testuser@gmail.com")
    user.set_password("testpassword")
    user.save()
    
    assert user.check_password("testpassword")
    assert not user.check_password("wrongpassword")

def test_save_user(test_client):
    user = User(username="testuser", email="testuser@gmail.com")
    user.set_password("testpassword")
    user.save()
    
    fetched_user = User.query.get(user.id)
    assert fetched_user is not None
    assert fetched_user.username == "testuser"

def test_delete_user(test_client):
    user = User(username="testuser", email="testuser@gmail.com")
    user.set_password("testpassword")
    user.save()
    
    user_id = user.id
    user.delete()
    
    fetched_user = User.query.get(user_id)
    assert fetched_user is None