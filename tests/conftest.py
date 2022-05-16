import json
import pytest
from config import create_app_test, db
from werkzeug.security import generate_password_hash
from models.user import User


from .settings import Config


@pytest.fixture()
def app():
    app = create_app_test(config=Config)
    app.config['TESTING'] = True
    app.app_context().push()
    db.create_all()
    yield app


@pytest.fixture()
def superuser():
    hash_password = generate_password_hash('password123', method='sha256')
    superuser = User(login='admin', password=hash_password, is_admin=True)
    db.session.add(superuser)
    db.session.commit()


@pytest.fixture()
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture()
def session():
    yield db.session
    db.session.remove()
    db.drop_all()


@pytest.fixture()
def create(client):
    data = json.dumps(dict(login='user', password='userpass123'))
    response = client.post('/auth/v1/registration',
                           data=data,
                           content_type='application/json')
    yield response


@pytest.fixture()
def login_super_user(client, session):
    data = json.dumps(dict(login='admin', password='password123'))

    response = client.post('/auth/v1/login',
                           data=data,
                           content_type='application/json')

    tokens = dict(user=response.json['user'],
                  access_token=response.json['access_token'],
                  refresh_token=response.json['refresh_token'])

    yield tokens


@pytest.fixture()
def login(client, session):
    data = json.dumps(dict(login='user', password='userpass123'))

    response = client.post('/auth/v1/login',
                           data=data,
                           content_type='application/json')

    tokens = dict(user=response.json['user'],
                  access_token=response.json['access_token'],
                  refresh_token=response.json['refresh_token'])

    yield tokens


@pytest.fixture()
def role_create(client, superuser, login_super_user, session):
    user = login_super_user
    data = json.dumps(dict(name='standart', role_description='Detailed description of the role'))

    response = client.post('/auth/v1/roles',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})
    return response


@pytest.fixture()
def delete_user_role(client, superuser, login_super_user, role_create, session):
    user = login_super_user
    data = json.dumps(dict(role_name='standart'))
    response = client.post(f'/auth/v1/user/{user["user"]}/add-role',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})

    return response


@pytest.fixture()
def role_id(client, superuser, login_super_user, role_create, session):
    user = login_super_user
    response = client.get(f'/auth/v1/roles',
                          content_type='application/json',
                          headers={'Authorization': f'Bearer {user["access_token"]}'})
    return response


@pytest.fixture()
def create_permission(client, superuser, login_super_user, session):
    user = login_super_user
    data = json.dumps(dict(name='basic', permission_description="Detailed description of the permission"))
    response = client.post(f'/auth/v1/permission',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})

    return response


@pytest.fixture()
def permission_to_role(client, superuser, login_super_user, role_create, role_id, create_permission, session):
    user = login_super_user
    role_id = role_id.json['role_list'][0]['id']
    data = json.dumps(dict(permission_name='basic'))
    response = client.post(f'/auth/v1/roles/{role_id}/add-permission',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})

    return dict(role_id=role_id,
                access_token=user["access_token"],
                response=response)
