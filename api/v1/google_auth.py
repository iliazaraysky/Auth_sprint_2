import os
import flask
import string
import random
import pathlib
from config import db
from models.user import User, SocialAccount, UserHistory
from werkzeug.security import generate_password_hash, check_password_hash

from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token)

from flask import Blueprint
from flask import redirect, session

import google_auth_oauthlib.flow
import googleapiclient.discovery

# client_secret_google.json у каждого свой,
# скачивается, когда создается приложение в Google Cloud Platform

CLIENT_SECRETS_FILE = os.path.join(pathlib.Path(__file__).parent,
                                   'client_secret_google.json')

SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']

blueprint = Blueprint('google_oauth', __name__, url_prefix='/auth/v1/google')
API_VERSION = 'v1'


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


@blueprint.route('/authorize')
def google_authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid'],
        redirect_uri='http://127.0.0.1/auth/v1/google/oauth2callback'
    )

    authorization_url, state = flow.authorization_url(
        include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)


@blueprint.route('/oauth2callback')
def google_oauth2callback():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid'],
        state=state
    )
    flow.redirect_uri = 'http://127.0.0.1/auth/v1/google/oauth2callback'

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    service = googleapiclient.discovery.build('people', API_VERSION,
                                              credentials=credentials)

    # Помимо создания приложения я открыл доступ к People API
    # Через него мне было понятнее получить данные пользователя
    # https://developers.google.com/people/v1/profiles?hl=en_US

    profile = service.people().get(
        resourceName='people/me',
        personFields='names,emailAddresses'
    ).execute()

    profile_data = dict(
        email=profile['emailAddresses'][0]['value'],
        social_id=profile['resourceName'],
        first_name=profile['names'][0]['givenName'],
        last_name=profile['names'][0]['familyName']
    )

    # Выбор, логин или создание пользователя
    # происходит в функции social_create_or_login

    return social_create_or_login(profile_data)
