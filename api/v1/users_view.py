import os
import click
import redis
from functools import wraps
from config import db, jwt
from dotenv import load_dotenv
from datetime import timedelta
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (get_jwt,
                                jwt_required,
                                get_jwt_identity,
                                create_access_token,
                                create_refresh_token,
                                verify_jwt_in_request)

from models.role import Role, UserRole
from models.user import User, UserHistory

load_dotenv()

blueprint = Blueprint('users', __name__, url_prefix='/auth/v1')
tfaablueprint = Blueprint('2fa', __name__, url_prefix='/auth/v1')
blueprint_admin_create = Blueprint('admin', __name__, cli_group=None)

jwt_redis_blocklist = redis.StrictRedis(host=os.getenv("REDIS_HOST"),
                                        port=os.getenv("REDIS_PORT"),
                                        db=0, decode_responses=True)


@blueprint_admin_create.cli.command('createsuperuser')
@click.argument('name')
@click.argument('password')
def create_superuser(name, password):
    hash_password = generate_password_hash(password, method='sha256')
    superuser = User(login=name, password=hash_password, is_admin=True)
    db.session.add(superuser)
    db.session.commit()
    return 'Superuser created'


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@blueprint.route('/hello')
def hello():
    return "Hello"


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if claims['is_administrator']:
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Admins only!"), 403
        return decorator
    return wrapper


@blueprint.route('/registration', methods=['POST'])
def create_user():
    data = request.get_json()
    hash_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(login=data['login'], password=hash_password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created'})


@blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(login=data['login']).first()
    user_id = str(user.id)
    user_name = str(user.login)
    user_agent = request.headers.get('user-agent', '')
    user_host = request.headers.get('host', '')
    user_info = UserHistory(user_id=user_id,
                            user_name=user_name,
                            user_agent=user_agent,
                            ip_address=user_host,
                            user_auth_service='site')

    if user is None:
        return jsonify({'message:': 'User is not found'})

    if check_password_hash(user.password, data['password']):

        if user.is_admin == True:
            access_token = create_access_token(identity=user.id,
                                               additional_claims={"is_administrator": True})
            refresh_token = create_refresh_token(identity=user.id)

        if user.is_admin == False:
            access_token = create_access_token(identity=user.id,
                                               additional_claims={"is_administrator": False})
            refresh_token = create_refresh_token(identity=user.id)

        db.session.add(user_info)
        db.session.commit()

        return jsonify(message='Successful Entry',
                       user=user_id,
                       access_token=access_token,
                       refresh_token=refresh_token)
    return jsonify({'message': 'Wrong password'})


@blueprint.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, "", ex=timedelta(minutes=5))
    return jsonify(message="Access token revoked")


@blueprint.route('/user/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@blueprint.route('/user/change-password/<uuid:user_uuid>', methods=['PATCH'])
@jwt_required()
def change_password(user_uuid):
    data = request.get_json()

    user = User.query.filter_by(id=user_uuid).first()

    if user is None:
        return jsonify({'message': 'User not found. Check uuid'})

    old_password = data['old_password']
    new_password = data['new_password']

    if check_password_hash(user.password, old_password):
        hash_password = generate_password_hash(new_password, method='sha256')
        user.password = hash_password
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'})

    return jsonify({'message': 'You entered the wrong old password'})


@blueprint.route('/user/<uuid:user_uuid>', methods=['GET'])
@jwt_required()
def get_user_info(user_uuid):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    data = UserHistory.query.filter_by(
        user_id=str(user_uuid)).paginate(page=page, per_page=per_page)
    history = []
    for row in data.items:
        history.append({
            'id': row.id,
            'user_name': row.user_name,
            'user_agent': row.user_name,
            'ip_address': row.ip_address,
            'created': row.created
        })
    meta = {
        'page': data.page,
        'pages': data.pages,
        'total_objects': data.total,
        'prev_page': data.prev_num,
        'next_page': data.next_num
    }
    return jsonify(message='User login history',
                   user_login_history=history,
                   meta=meta)


@blueprint.route('/user/<uuid:user_uuid>/add-role', methods=['POST'])
@jwt_required()
@admin_required()
def add_user_role(user_uuid):
    data = request.get_json()
    user = User.query.filter_by(id=user_uuid).first()
    role = Role.query.filter_by(name=data['role_name']).first()
    user_role = UserRole(user=user.id, role=role.id)
    db.session.add(user_role)
    db.session.commit()

    return jsonify(message='Role for User created')


@blueprint.route('/user/<uuid:user_uuid>/delete-role', methods=['POST'])
@jwt_required()
@admin_required()
def delete_user_role(user_uuid):
    data = request.get_json()
    user = User.query.filter_by(id=user_uuid).first()
    role = Role.query.filter_by(name=data['role_name']).first()
    user_role = UserRole.query.filter_by(user=user.id, role=role.id).first()
    db.session.delete(user_role)
    db.session.commit()

    return jsonify(message='Role for User deleted')
