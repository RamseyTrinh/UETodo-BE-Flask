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
    MAIL_DEFAULT_SENDER = "minhnguyenhai26032003@gmail.com"
    MAIL_SUBJECT_PREFIX = "[MY RESTAURANT]"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.environ.get("AWS_REGION")
    AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
    ACCOUNT_NUMBER = os.environ.get("ACCOUNT_NUMBER")
    BANK = os.environ.get("BANK")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "your_cloud_name")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "your_api_key")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "your_api_secret")


secret_key = Config.SECRET_KEY
