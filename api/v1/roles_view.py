from config import db
from models.role import Role
from sqlalchemy import select
from .users_view import admin_required
from flask_jwt_extended import jwt_required
from flask import request, jsonify, Blueprint


blueprint = Blueprint('roles', __name__, url_prefix='/auth/v1')


@blueprint.route('/roles', methods=['POST'])
@jwt_required()
@admin_required()
def create_role():
    data = request.get_json()
    new_role = Role(name=data['name'], role_description=data['role_description'])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'message': 'New role created'})


@blueprint.route('/roles', methods=['GET'])
@jwt_required()
@admin_required()
def roles_list():
    data = select(Role.id, Role.name, Role.role_description)
    data_select = db.session.execute(data)
    data_select = data_select.fetchall()
    roles_list = [dict(row) for row in data_select]
    return jsonify(role_list=roles_list)


@blueprint.route('/roles/<uuid:role_uuid>', methods=['PATCH'])
@jwt_required()
@admin_required()
def edit_role(role_uuid):
    data = request.get_json()

    if len(data["name"]) == 0:
        return jsonify({'message': 'The name field cannot be empty'})

    role = Role.query.filter_by(id=role_uuid).first()

    if role is None:
        return jsonify({'message': 'Role not found. Check uuid'})

    Role.query.filter_by(id=role_uuid).update(data)
    db.session.commit()

    return jsonify(message='Role edited')


@blueprint.route('/roles/<uuid:role_uuid>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_role(role_uuid):
    role = Role.query.filter_by(id=role_uuid).first()

    if role is None:
        return jsonify({'message': 'Role not found. Check uuid'})

    Role.query.filter_by(id=role_uuid).delete()
    db.session.commit()

    return jsonify(message='Role delete')
