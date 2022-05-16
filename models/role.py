import uuid
import datetime
from config import db
from sqlalchemy.dialects.postgresql import UUID


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.VARCHAR(20), unique=True, nullable=False)
    role_description = db.Column(db.VARCHAR(100), nullable=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'{self.name}. {self.role_description}'


class UserRole(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), default=uuid.uuid4(), nullable=False)
    role = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), default=uuid.uuid4(), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
