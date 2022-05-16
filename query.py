from app import app
from db.sqlalchemy_data import db, init_db
from models.user import User

# Подготоваливаем контекст и создаём таблицы
init_db(app)
app.app_context().push()
db.create_all()

# Insert-запросы
admin = User(login='admin1423', password='password')
db.session.add(admin)
db.session.commit()

# Select-запросы
User.query.all()
User.query.filter_by(login='admin1423').first()
