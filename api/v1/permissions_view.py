from config import db
from flask_jwt_extended import jwt_required
from flask import request, jsonify, Blueprint

from .users_view import admin_required
from models.role import Role
from models.permission import Permission, RolePermission


blueprint = Blueprint('permissions', __name__, url_prefix='/auth/v1')


@blueprint.route('/permission', methods=['POST'])
@jwt_required()
@admin_required()
def create_permission():
    data = request.get_json()
    new_permission = Permission(name=data['name'],
                                permission_description=data['permission_description'])
    db.session.add(new_permission)
    db.session.commit()
    return jsonify({'message': 'New permission created'})


@blueprint.route('/roles/<uuid:role_uuid>/add-permission', methods=['POST'])
@jwt_required()
@admin_required()
def add_permission_role(role_uuid):
    data = request.get_json()
    role = Role.query.filter_by(id=role_uuid).first()
    permission = Permission.query.filter_by(name=data['permission_name']).first()
    role_permission = RolePermission(permission=permission.id, role=role.id)
    db.session.add(role_permission)
    db.session.commit()

    return jsonify('Permission for Role created')


@blueprint.route('/roles/<uuid:role_uuid>/delete-permission', methods=['POST'])
@jwt_required()
@admin_required()
def delete_permission_role(role_uuid):
    data = request.get_json()
    role = Role.query.filter_by(id=role_uuid).first()
    permission = Permission.query.filter_by(name=data['permission_name']).first()
    role_permission = RolePermission.query.filter_by(permission=permission.id, role=role.id).first()
    db.session.delete(role_permission)
    db.session.commit()

    return jsonify('Permission for Role deleted')
