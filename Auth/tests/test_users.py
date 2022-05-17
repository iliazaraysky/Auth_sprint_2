import json
from http import HTTPStatus


def test_user_registration(client):
    data = json.dumps(dict(login='user', password='userpass123'))
    response = client.post('/auth/v1/registration',
                           data=data,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.OK


def test_user_login(client, session):
    data = json.dumps(dict(login='user', password='userpass123'))
    response = client.post('/auth/v1/login',
                           data=data,
                           content_type='application/json')

    assert response.status_code == HTTPStatus.OK


def test_refresh_token(client, create, login, session):
    user = login
    data = json.dumps(dict(login='user', password='userpass123'))
    response = client.post('/auth/v1/user/token/refresh',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["refresh_token"]}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json['access_token'] != user['access_token']


def test_password_change(client, create, login, session):
    user = login
    data = json.dumps(dict(old_password='userpass123', new_password='userpass1234'))
    response = client.patch(f'/auth/v1/user/change-password/{user["user"]}',
                            data=data,
                            content_type='application/json',
                            headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK


def test_get_user_history(client, create, login, session):
    user = login
    response = client.get(f'/auth/v1/user/{user["user"]}',
                          content_type='application/json',
                          headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json['user_login_history'][0]['user_name'] == 'user'


def test_logout_user(client, create, login, session):
    user = login
    response = client.delete('/auth/v1/logout',
                             content_type='application/json',
                             headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json['message'] == 'Access token revoked'


def test_add_user_role(client, superuser, login_super_user, role_create, session):
    user = login_super_user
    data = json.dumps(dict(role_name='standart'))
    response = client.post(f'/auth/v1/user/{user["user"]}/add-role',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK


def test_delete_user_role(client, superuser, login_super_user, role_create, delete_user_role, session):
    user = login_super_user
    data = json.dumps(dict(role_name='standart'))
    response = client.post(f'/auth/v1/user/{user["user"]}/delete-role',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK
