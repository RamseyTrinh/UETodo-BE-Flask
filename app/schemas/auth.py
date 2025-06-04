from flask_restx import Namespace, fields


class AuthSchema:
    api = Namespace("auth", description="Authentication related operations")
    login_model = api.model(
        "Login",
        {
            "email": fields.String(required=True, description="User email"),
            "password": fields.String(required=True, description="User password"),
        },
    )

    create_user_model = api.model(
        "CreateUser",
        {
            "email": fields.String(required=True, description="User email"),
            "password": fields.String(required=True, description="User password"),
            "name": fields.String(required=True, description="Full name"),
            "dob": fields.String(
                required=True, description="Date of birth (yyyy-mm-dd)"
            ),
            "gender": fields.String(
                required=True, description="Gender (Male/Female/Other)"
            ),
            "phone_number": fields.String(required=True, description="Phone number"),
        },
    )

    register_model = api.model(
        "Register",
        {
            "email": fields.String(required=True, description="User email"),
            "password": fields.String(required=True, description="User password"),
            "name": fields.String(required=True, description="Full name"),
            "dob": fields.String(
                required=True, description="Date of birth (yyyy-mm-dd)"
            ),
            "gender": fields.String(
                required=True, description="Gender (Male/Female/Other)"
            ),
            "phone_number": fields.String(required=True, description="Phone number"),
        },
    )

    refresh_token_model = api.model(
        "RefreshToken",
        {"refresh_token": fields.String(required=True, description="Refresh token")},
    )

    logout_model = api.model(
        "Logout", {"user_id": fields.Integer(required=True, description="User ID")}
    )

    email_model = api.model(
        "EmailOnly", {"email": fields.String(required=True, description="User email")}
    )

    verify_email_model = api.model(
        "VerifyEmail",
        {
            "confirm_token": fields.String(
                required=True, description="Confirm token sent to email"
            ),
            "verification_code": fields.String(
                required=True, description="Verification code sent to email"
            ),
        },
    )

    reset_password_request_model = api.model(
        "ResetPasswordRequest",
        {"email": fields.String(required=True, description="User email")},
    )

    reset_password_verify_model = api.model(
        "ResetPasswordVerify",
        {
            "confirm_token": fields.String(required=True, description="Reset token"),
            "verification_code": fields.String(required=True, description="Reset code"),
        },
    )
    
    new_password_model = api.model(
        "NewPassword",
        {
            "email": fields.String(required=True, description="User email"),
            "confirm_token": fields.String(
                required=True, description="Reset token"
            ),
            "new_password": fields.String(required=True, description="New password"),
            "confirm_password": fields.String(
                required=True, description="Confirm new password"
            ),
        },
    )
