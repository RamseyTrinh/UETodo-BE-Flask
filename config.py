import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret_key")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")

    POSTGRESQL_USERNAME = os.environ.get("POSTGRESQL_USERNAME")
    POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
    POSTGRESQL_HOST = os.environ.get("POSTGRESQL_HOST")
    POSTGRESQL_PORT = os.environ.get("POSTGRESQL_PORT")
    POSTGRESQL_DBNAME = os.environ.get("POSTGRESQL_DBNAME")
    SQLALCHEMY_DATABASE_URI = (
            os.environ.get("DATABASE_URL")
            or f"postgresql://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DBNAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "hoangkmhd190@gmail.com"
    MAIL_SUBJECT_PREFIX = "[UETodo App]"


secret_key = Config.SECRET_KEY
