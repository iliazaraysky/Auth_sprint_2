from flasgger import Schema, fields


class Registration(Schema):
    login = fields.Str()
    password = fields.Str()


class Login(Schema):
    login = fields.Str()
    password = fields.Str()


class Logout(Schema):
    refresh_token = fields.Str()


class RefreshToken(Schema):
    refresh_token = fields.Str()


class ChangePassword(Schema):
    old_password = fields.Str()
    new_password = fields.Str()


class UserHistory(Schema):
    access_token = fields.Str()


class UserRole(Schema):
    role = fields.Str()


class Role(Schema):
    name = fields.Str()
    role_description = fields.Str()


class RoleId(Schema):
    role_uuid = fields.Str()


class Permission(Schema):
    name = fields.Str()
    permission_description = fields.Str()


class RolePermission(Schema):
    role = fields.Str()
    permission = fields.Str()
