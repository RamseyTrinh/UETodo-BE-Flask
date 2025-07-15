from celery import Celery
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from config import Config
from .exceptions import base_exception
from .schemas import AuthSchema, UserSchema, TaskSchema


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
mail = Mail()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
blueprint = Blueprint("api", __name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config["SPEC_FORMAT"] = "yaml"
    app.config.from_object(config_class)
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*": { 
                "origins": ["http://app.uetodo.site", "http://localhost:3000"],
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "X-Requested-With",
                    "Accept",
                ],
                "expose_headers": ["Authorization", "Content-Length"],
            }
        },
    )

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    celery.conf.update(app.config)
    
    from app.controllers import (
        auth_api,
        user_api,
        task_api,
    )

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        },
        "Basic Auth": {
            "type": "basic",
            "description": "Basic Auth using username and password"
        }
    }
    app.register_blueprint(blueprint)
    api = Api(
        app,
        title="UETodo APIs",
        version="1.0",
        description="APIs",
        prefix="/api/v1",
        authorizations=authorizations,
        security=[],
    )
    api.add_namespace(AuthSchema.api, path="/auth")
    api.add_namespace(UserSchema.api, path="/user")
    api.add_namespace(TaskSchema.api, path="/task")

    app.register_error_handler(Exception, base_exception)

    return app
