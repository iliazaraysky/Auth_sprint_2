import string
import random
from config import db
from config.settings import GoogleOAuth
from config import oauth
from flask import url_for
from models.user import User, SocialAccount, UserHistory
from werkzeug.security import generate_password_hash

from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token)

blueprint = Blueprint('google_oauth', __name__, url_prefix='/auth/v1/google')\

google = oauth.register(
    name=GoogleOAuth.GOOGLE_NAME,
    server_metadata_url=GoogleOAuth.GOOGLE_SERVER_META_DATA_URL,
    client_id=GoogleOAuth.GOOGLE_CLIENT_ID,
    client_secret=GoogleOAuth.GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid profile email'}
)


def generate_random_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    password = []
    for i in range(6):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)


def create_tokens(user):
    access_token = create_access_token(identity=user.id,
                                       additional_claims={
                                           "is_administrator": False})
    refresh_token = create_refresh_token(identity=user.id)
    tokens = dict(access_token=access_token, refresh_token=refresh_token)
    return tokens


def user_auth_history(user):
    user_id = str(user.id)
    user_name = str(user.login)
    user_agent = request.headers.get('user-agent', '')
    user_host = request.headers.get('host', '')
    user_info = UserHistory(user_id=user_id,
                            user_name=user_name,
                            user_agent=user_agent,
                            ip_address=user_host,
                            user_auth_service='social')

    db.session.add(user_info)
    db.session.commit()


def social_create_or_login(profile_data):
    hash_password = generate_password_hash(
        generate_random_password(),
        method='sha256'
    )

    social_account = SocialAccount.query.filter_by(
        social_id=profile_data['social_id']).one_or_none()
    if social_account is not None:
        user = social_account.user
    else:
        new_user = User(login=profile_data['last_name'],
                        email=profile_data['email'],
                        password=hash_password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        new_user_id = User.query.filter_by(
            login=profile_data['last_name']).first()
        social_account = SocialAccount(
            user_id=new_user_id.id,
            user=new_user_id,
            social_id=profile_data['social_id'],
            social_name=profile_data['first_name']
        )
        db.session.add(social_account)
        db.session.commit()

        # Создаем токены для нового пользователя
        tokens = create_tokens(new_user_id)

        # Записываем историю входа
        user_auth_history(new_user_id)

        return jsonify(message='Successful Entry',
                       user=new_user_id.id,
                       access_token=tokens['access_token'],
                       refresh_token=tokens['refresh_token'])

    # Создаем токены для существующего пользователя
    tokens = create_tokens(user)

    # Записываем историю входа
    user_auth_history(user)
    return jsonify(message='Successful Entry',
                   user=user.id,
                   access_token=tokens['access_token'],
                   refresh_token=tokens['refresh_token'])


@blueprint.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_oauth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@blueprint.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user = token['userinfo']

    profile_data = dict(
        email=user['email'],
        social_id=user['sub'],
        first_name=user['given_name'],
        last_name=user['family_name']
    )

    # Выбор, логин или создание пользователя
    # происходит в функции social_create_or_login
    # return redirect('/')
    return social_create_or_login(profile_data)
