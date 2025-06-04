from flask_restx import Namespace, fields, reqparse


class UserSchema:
    api = Namespace("user", description="User related operations")
    user_model = api.model(
        "User",
        {
            "email": fields.String(required=True),
            "name": fields.String(required=True),
            "dob": fields.String(required=True, description="YYYY-MM-DD"),
            "gender": fields.String(required=True),
            "phone_number": fields.String(required=True),
            "avatar_url": fields.String(default=""),
            "is_verified": fields.Boolean(default=False),
        },
    )
    password_update_model = api.model(
        "PasswordUpdate",
        {
            "old_password": fields.String(required=True),
            "new_password": fields.String(required=True),
        },
    )
    create_user_model = reqparse.RequestParser()
    create_user_model.add_argument("email", type=str, required=True, location="form")
    create_user_model.add_argument("password", type=str, required=True, location="form")
    create_user_model.add_argument("name", type=str, required=True, location="form")
    create_user_model.add_argument(
        "dob", type=str, required=True, location="form"
    )  # YYYY-MM-DD
    create_user_model.add_argument("gender", type=str, required=True, location="form")
    create_user_model.add_argument(
        "phone_number", type=str, required=True, location="form"
    )
    create_user_model.add_argument(
        "avatar", type="FileStorage", location="files", required=False
    )
    new_password_model = api.model(
        "NewPassword",
        {
            "email": fields.String(required=True, description="User email"),
            "new_password": fields.String(required=True, description="New password"),
        },
    )
