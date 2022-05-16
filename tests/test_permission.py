import json
from http import HTTPStatus


def test_create_permission(client, superuser, login_super_user, session):
    user = login_super_user
    data = json.dumps(dict(name='basic', permission_description="Detailed description of the permission"))
    response = client.post(f'/auth/v1/permission',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK


def test_add_permission_to_role(client, superuser, login_super_user, role_create, role_id, create_permission, session):
    user = login_super_user
    role_id = role_id.json['role_list'][0]['id']
    data = json.dumps(dict(permission_name='basic'))
    response = client.post(f'/auth/v1/roles/{role_id}/add-permission',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {user["access_token"]}'})

    assert response.status_code == HTTPStatus.OK


def test_delete_permission_from_role(client, permission_to_role, session):
    permission_to_role = permission_to_role
    data = json.dumps(dict(permission_name='basic'))
    response = client.post(f'/auth/v1/roles/{permission_to_role["role_id"]}/delete-permission',
                           data=data,
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {permission_to_role["access_token"]}'})

    assert response.status_code == HTTPStatus.OK
