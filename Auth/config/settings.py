import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = 'secret'
    JWT_SECRET_KEY = 'secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=60)

    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("POSTGRES_DB")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class GoogleOAuth:
    GOOGLE_NAME: str = os.getenv('GOOGLE_NAME')
    GOOGLE_SERVER_META_DATA_URL: str = os.getenv('GOOGLE_SERVER_META_DATA_URL')
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET')
