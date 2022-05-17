import json
from http import HTTPStatus


def test_get_roles_list(client, superuser, login_super_user, role_create, session):
    user = login_super_user
    response = client.get(f'/auth/v1/roles',
                          content_type='application/json',
                          headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK


def test_edit_role(client, superuser, login_super_user, role_create, role_id, session):
    user = login_super_user
    role_id = role_id.json['role_list'][0]["id"]

    data = json.dumps(dict(name='standart user'))
    response = client.patch(f'/auth/v1/roles/{role_id}',
                            data=data,
                            content_type='application/json',
                            headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK


def test_delete_role(client, superuser, login_super_user, role_create, role_id, session):
    user = login_super_user
    role_id = role_id.json['role_list'][0]["id"]

    response = client.delete(f'/auth/v1/roles/{role_id}',
                             content_type='application/json',
                             headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK
