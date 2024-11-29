# from app.users.models import User

def test_register_user(test_client):
    response = test_client.post("/auth/register", json={"username": "testuser", "email": "testuser@gmail.com", "password": "testpassword"})
    assert response.status_code == 201
    assert response.get_json() == {"Message": "User created"}

def test_register_user_already_exists(test_client):
    test_client.post("/auth/register", json={"username": "testuser", "email": "testuser@gmail.com", "password": "testpassword"})
    response = test_client.post("/auth/register", json={"username": "testuser", "email": "testuser@gmail.com", "password": "testpassword"})
    assert response.status_code == 403
    assert response.get_json() == {"error": "User already exists"}

def test_login_user(test_client):
    test_client.post("/auth/register", json={"username": "testuser", "email": "testuser@gmail.com", "password": "testpassword"})
    response = test_client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "tokens" in response.get_json()

def test_login_user_invalid_credentials(test_client):
    response = test_client.post("/auth/login", json={"username": "wronguser", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid username or password"}

def test_whoami(test_client):
    test_client.post("/auth/register", json={"username": "testuser", "email": "testuser@gmail.com", "password": "testpassword"})
    login_response = test_client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    access_token = login_response.get_json()["tokens"]["access"]
    response = test_client.get("/auth/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.get_json()["user_details"]["username"] == "testuser"

def test_refresh_access(test_client):
    test_client.post("/auth/register", json={"username": "testuser", "email": "testuser@gmail.com", "password": "testpassword"})
    login_response = test_client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    refresh_token = login_response.get_json()["tokens"]["refresh"]
    response = test_client.get("/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    assert "acces_token" in response.get_json()

def test_logout_user(test_client):
    test_client.post("/auth/register", json={"username": "testuser", "email": "testuser@gmail.com", "password": "testpassword"})
    login_response = test_client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    access_token = login_response.get_json()["tokens"]["access"]
    response = test_client.get("/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "access token revoked successfully"}