from flask import request
from flask_restx import Resource
from validate_email_address import validate_email

from app.schemas import AuthSchema
from app.services import AuthService
from app.utils.decorators import JWT_required
from app.utils.email import send_email

auth_api = AuthSchema.api


@auth_api.route("/login")
class LoginController(Resource):
    @auth_api.expect(AuthSchema.login_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400

        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return {
                "success": False,
                "message": "Email and password are required.",
            }, 400

        if not validate_email(email):
            return {"success": False, "message": "Invalid email address."}, 400

        auth_service = AuthService()
        user = auth_service.validate_login(email, password)
        if not user:
            return {"success": False, "message": "Bad email or password."}, 400

        access_token = auth_service.generate_access_token(user.id)
        refresh_token = auth_service.generate_refresh_token(user.id)
        return {
            "success": True,
            "message": "Login successful.",
            "user": user.as_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200


@auth_api.route("/create-user")
class CreateUserController(Resource):
    @auth_api.expect(AuthSchema.create_user_model)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400

        REQUIRED_FIELDS = {
            "email",
            "password",
            "name",
            "dob",
            "gender",
            "phone_number",
        }
        missing_fields = {field for field in REQUIRED_FIELDS if data.get(field) is None}
        if missing_fields:
            return {
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}",
            }, 400

        if not validate_email(data["email"]):
            return {"success": False, "message": "Invalid email address."}, 400

        auth_service = AuthService()
        existed_user = auth_service.check_email_registered(data["email"])
        if existed_user:
            return {"success": False, "message": "Email is already registered."}, 400

        new_user = auth_service.save(
            data["email"],
            data["password"],
            data["name"],
            data["dob"],
            data["gender"],
            data["phone_number"],
        )
        return new_user.as_dict(), 201


@auth_api.route("/register")
class RegisterController(Resource):
    @auth_api.expect(AuthSchema.register_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400

        REQUIRED_FIELDS = {"email", "password", "name", "dob", "gender", "phone_number"}
        missing_fields = {field for field in REQUIRED_FIELDS if data.get(field) is None}
        if missing_fields:
            return {
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}",
            }, 400

        if not validate_email(data["email"]):
            return {"success": False, "message": "Invalid email address."}, 400

        auth_service = AuthService()
        existed_user = auth_service.check_email_registered(data["email"])
        if existed_user:
            return {"success": False, "message": "Email is already registered."}, 400

        new_user = auth_service.save(
            data["email"],
            data["password"],
            data["name"],
            data["dob"],
            data["gender"],
            data["phone_number"],
        )
        verification_code = auth_service.generate_verification_code(new_user.email)
        confirm_token = auth_service.generate_confirm_token(new_user.email)
        # send_email(
        #     to=data["email"],
        #     subject="Your Verification Code from 4M Library",
        #     template="confirm",
        #     user=new_user,
        #     code=verification_code,
        # )
        return {
            "success": True,
            "message": "User registered successfully. An email has been sent to confirm your account.",
            "user": new_user.as_dict(),
            "confirm_token": confirm_token,
        }, 201


@auth_api.route("/refresh-token")
class RefreshTokenController(Resource):
    @auth_api.doc(
        "Refresh Token API",
    )
    @auth_api.expect(AuthSchema.refresh_token_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400

        refresh_token = data.get("refresh_token")
        if refresh_token is None:
            return {"success": False, "message": "Refresh token is required."}, 400

        auth_service = AuthService()
        user_id = auth_service.verify_refresh_token(refresh_token)
        if user_id is None:
            return {
                "success": False,
                "message": "Invalid or expired refresh token.",
            }, 400

        new_access_token = auth_service.generate_access_token(user_id)
        new_refresh_token = auth_service.generate_refresh_token(user_id)
        return {
            "success": True,
            "message": "Token refreshed.",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }, 200


@auth_api.route("/logout")
class LogoutController(Resource):
    @auth_api.doc(
        "Logout API",
    )
    @JWT_required
    def post(self, user_id):
        auth_service = AuthService()
        if auth_service.invalidate_refresh_token(user_id):
            return "", 204

        return {"success": False, "message": "Failed to log out. Invalid token."}, 401


# @auth_api.route("/send-verification-code")
# class SendVerificationCodeController(Resource):
#     @auth_api.expect(AuthSchema.email_model, validate=True)
#     def post(self):
#         data = request.get_json()
#         if not data:
#             return {"success": False, "message": "Invalid JSON data."}, 400

#         email = data.get("email")
#         if not email:
#             return {"success": False, "message": "Email is required."}, 400

#         if not validate_email(email):
#             return {"success": False, "message": "Invalid email address."}, 400

#         auth_service = AuthService()
#         registered_user = auth_service.check_email_registered(email)
#         if not registered_user:
#             return {"success": False, "message": "Email is not registered."}, 400

#         if auth_service.is_verified(email):
#             return {"success": False, "message": "Email is already verified."}, 400

#         verification_code = auth_service.generate_verification_code(email)
#         confirm_token = auth_service.generate_confirm_token(email)
#         send_email(
#             to=data["email"],
#             subject="Your Verification Code from UETodo App",
#             template="confirm",
#             user=registered_user,
#             code=verification_code,
#         )

#         return {
#             "success": True,
#             "message": "Verification code sent to email successfully.",
#             "confirm_token": confirm_token,
#         }, 200


# @auth_api.route("/verify-email")
# class VerifyEmailController(Resource):
#     @auth_api.expect(AuthSchema.verify_email_model, validate=True)
#     def post(self):
#         data = request.get_json()
#         if not data:
#             return {"success": False, "message": "Invalid JSON data."}, 400

#         confirm_token = data.get("confirm_token")
#         verification_code = data.get("verification_code")
#         if not confirm_token or not verification_code:
#             return {
#                 "success": False,
#                 "message": "Confirm token and verification code are required.",
#             }, 400

#         auth_service = AuthService()
#         user = auth_service.verify_verification_code(confirm_token, verification_code)
#         if user and auth_service.verify_user_email(user.email):
#             access_token = auth_service.generate_access_token(user.id)
#             refresh_token = auth_service.generate_refresh_token(user.id)
#             return {
#                 "success": True,
#                 "message": "Your email address was verified successfully.",
#                 "access_token": access_token,
#                 "refresh_token": refresh_token,
#             }, 200
#         else:
#             return {
#                 "success": False,
#                 "message": "Invalid confirm token or verification code.",
#             }, 400


@auth_api.route("/reset-password")
class RequestResetPasswordController(Resource):
    @auth_api.expect(AuthSchema.reset_password_request_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400

        email = data.get("email")
        if not email:
            return {"success": False, "message": "Email is required."}, 400

        if not validate_email(email):
            return {"success": False, "message": "Invalid email address."}, 400

        auth_service = AuthService()
        registered_user = auth_service.check_email_registered(email)
        if not registered_user:
            return {"success": False, "message": "Email is not registered."}, 400

        reset_code = auth_service.generate_reset_code(email)
        reset_token = auth_service.generate_reset_token(email)
        send_email(
            to=email,
            subject="Reset Your Password from UETodo",
            template="reset-password",
            user=registered_user,
            code=reset_code,
        )

        return {
            "success": True,
            "message": "Verification code sent successfully to your email.",
            "confirm_token": reset_token,
        }, 200


@auth_api.route("/verify-reset-code")
class ValidateResetCodeController(Resource):
    @auth_api.expect(AuthSchema.reset_password_verify_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400

        reset_token = data.get("confirm_token")
        reset_code = data.get("verification_code")
        if not reset_token or not reset_code:
            return {
                "success": False,
                "message": "Reset token and reset code are required.",
            }, 400

        auth_service = AuthService()
        user = auth_service.verify_reset_code(reset_token, reset_code)
        if user:
            temp_access_token = auth_service.generate_access_token(user.id)
            return {
                "success": True,
                "message": "Reset code verified successfully.",
                "temp_access_token": temp_access_token,
            }, 200
        else:
            return {
                "success": False,
                "message": "Invalid reset token or reset code.",
            }, 400
