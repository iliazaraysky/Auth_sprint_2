import uuid
import datetime
from config import db
from sqlalchemy.dialects.postgresql import UUID


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.VARCHAR(20), unique=True, nullable=False)
    permission_description = db.Column(db.VARCHAR(100), nullable=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    permission = db.Column(UUID(as_uuid=True), db.ForeignKey('permissions.id'), default=uuid.uuid4(), nullable=False)
    role = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), default=uuid.uuid4(), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
