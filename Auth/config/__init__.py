import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .settings import Config
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from authlib.integrations.flask_client import OAuth
from .jaeger import configure_tracer
from opentelemetry.instrumentation.flask import FlaskInstrumentor

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address, default_limits=['200/day', '50/hour'])
configure_tracer()
oauth = OAuth()


def create_app_test(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    config_blue(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    return app


def create_app(config=Config):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'Authentication Service. Sprint 7',
        'uiversion': 3
    }
    swagger = Swagger(app)
    app.config.from_object(config)
    config_blue(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    oauth.init_app(app)
    FlaskInstrumentor().instrument_app(app)

    from api.v1.swagger import swagger_view
    from api.v1 import VERSION_PREFIX

    app.add_url_rule('/auth' + VERSION_PREFIX + 'registration',
                     view_func=swagger_view.RegistrationView.as_view('registration'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'login',
                     view_func=swagger_view.LoginView.as_view('login'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'logout',
                     view_func=swagger_view.LogoutView.as_view('logout'),
                     methods=['DELETE'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'user/token/refresh',
                     view_func=swagger_view.RefreshToken.as_view('refresh'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'user/change-password/<uuid:user_uuid>',
                     view_func=swagger_view.ChangeUserPassword.as_view('change password'),
                     methods=['PATCH'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'user/<uuid:user_uuid>',
                     view_func=swagger_view.GetUserHistory.as_view('user hishory'),
                     methods=['GET'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'user/<uuid:user_uuid>/add-role',
                     view_func=swagger_view.AddUserRole.as_view('user role'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'user/<uuid:user_uuid>/delete-role',
                     view_func=swagger_view.DeleteUserRole.as_view('delete role'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'roles',
                     view_func=swagger_view.CreateRole.as_view('create role'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'roles',
                     view_func=swagger_view.GetRoleList.as_view('roles list'),
                     methods=['GET'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'roles/<uuid:role_uuid>',
                     view_func=swagger_view.EditRole.as_view('edit role'),
                     methods=['PATCH'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'roles/<uuid:role_uuid>',
                     view_func=swagger_view.DeleteRole.as_view('delete roles'),
                     methods=['DELETE'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'permission',
                     view_func=swagger_view.CreatePermission.as_view('create permission'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'roles/<uuid:role_uuid>/add-permission',
                     view_func=swagger_view.AddRolePermission.as_view('add role permission'),
                     methods=['POST'])

    app.add_url_rule('/auth' + VERSION_PREFIX + 'roles/<uuid:role_uuid>/delete-permission',
                     view_func=swagger_view.DeleteRolePermission.as_view('delete role permission'),
                     methods=['POST'])

    return app


def config_blue(app):
    from api.v1.users_view import blueprint as users_blueprint
    from api.v1.users_view import blueprint_admin_create as admin_blueprint
    from api.v1.users_view import tfaablueprint as two_factor_authentication
    from api.v1.roles_view import blueprint as roles_blueprint
    from api.v1.permissions_view import blueprint as permissions_blueprint

    from api.v1.google_auth import blueprint as google_oauth
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(roles_blueprint)
    app.register_blueprint(permissions_blueprint)
    app.register_blueprint(google_oauth)
    app.register_blueprint(two_factor_authentication)

    @app.route('/')
    def index():
        return "Google OAuth <a href='/auth/v1/google/authorize'><button> Login</button></a>"

