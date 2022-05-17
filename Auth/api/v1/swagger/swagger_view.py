from .schemas import *
from flasgger import SwaggerView


class RegistrationView(SwaggerView):
    tags = ['Authorization']
    parameters = [
        {
            'name': 'login',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'password',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'User registration',
            'schema': Registration
        }
    }


class LoginView(SwaggerView):
    tags = ['Authorization']
    parameters = [
        {
            'name': 'login',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'password',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'User login to the site',
            'schema': Login
        }
    }


class LogoutView(SwaggerView):
    tags = ['Authorization']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'Refresh token',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'User logs out',
            'schema': Logout
        }
    }


class RefreshToken(SwaggerView):
    tags = ['User']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'Refresh token',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'User logs out',
            'schema': RefreshToken
        },
        401: {
            'description': 'User is not authorized'
        }
    }


class ChangeUserPassword(SwaggerView):
    tags = ['User']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'old_password',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'new_password',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Change user password',
            'schema': ChangePassword
        },
        401: {
            'description': 'User is not authorized'
        }
    }


class GetUserHistory(SwaggerView):
    tags = ['User']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
    ]
    responses = {
        200: {
            'description': 'View User History',
            'schema': UserHistory
        },
        401: {
            'description': 'User is not authorized'
        }
    }


class AddUserRole(SwaggerView):
    tags = ['User']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'role',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Add role to user',
            'schema': UserRole
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }


class DeleteUserRole(SwaggerView):
    tags = ['User']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'role',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Add role to user',
            'schema': UserRole
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }


class CreateRole(SwaggerView):
    tags = ['Roles']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'role description',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Add role to user',
            'schema': UserRole
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }

    }


class GetRoleList(SwaggerView):
    tags = ['Roles']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'role uuid',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Get a list of roles',
            'schema': RoleId
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }


class EditRole(SwaggerView):
    tags = ['Roles']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': False,
        },
        {
            'name': 'role description',
            'in': 'body',
            'type': 'string',
            'required': False,
        }
    ]
    responses = {
        200: {
            'description': 'Edit role',
            'schema': Role
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }


class DeleteRole(SwaggerView):
    tags = ['Roles']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'role uuid',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Delete role',
            'schema': RoleId
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }


class CreatePermission(SwaggerView):
    tags = ['Permissions']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'permission description',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Create Permission',
            'schema': Permission
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }


class AddRolePermission(SwaggerView):
    tags = ['Permissions']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'permission',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Add Permission to a Role',
            'schema': RolePermission
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }


class DeleteRolePermission(SwaggerView):
    tags = ['Permissions']
    parameters = [
        {
            'name': 'Token',
            'in': 'header',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
        },
        {
            'name': 'permission',
            'in': 'body',
            'type': 'string',
            'required': True,
        }
    ]
    responses = {
        200: {
            'description': 'Removing a Role Permission',
            'schema': RolePermission
        },
        401: {
            'description': 'User is not authorized'
        },
        403: {
            'description': 'The user must have super user rights'
        }
    }
