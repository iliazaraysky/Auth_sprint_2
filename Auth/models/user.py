import uuid
import datetime
from config import db
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, nullable=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<User {self.login}>'


class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('social_accounts', lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'), )

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


def create_partition(target, connection, **kw) -> None:
    """ Создает партицирование в модели user_history.
        Не создается в автоматических миграциях,
        необходимо дописывать руками migrations/versions,
        перед выполнением команды flask db upgrade
     """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_history_site" PARTITION OF "user_history" FOR VALUES IN ('site')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_history_social" PARTITION OF "user_history" FOR VALUES IN ('social')"""
    )


class UserHistory(db.Model):
    __tablename__ = 'user_history'

    __table_args__ = (
        UniqueConstraint('id', 'user_auth_service'),
        {
            'postgresql_partition_by': 'LIST (user_auth_service)',
            'listeners': [('after_create', create_partition)],
        }
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user_name = db.Column(db.String, nullable=False)
    user_agent = db.Column(db.String, nullable=True)
    ip_address = db.Column(db.String, nullable=True)
    user_auth_service = db.Column(db.Text, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, user_id, user_name, user_agent, ip_address, user_auth_service):
        self.user_id = user_id
        self.user_name = user_name
        self.user_agent = user_agent,
        self.ip_address = ip_address,
        self.user_auth_service = user_auth_service
