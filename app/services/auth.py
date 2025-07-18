import logging
import random
from datetime import datetime, timezone, timedelta

import jwt
from werkzeug.security import check_password_hash

from app.repository import TokenRepository, UserRepository
from config import secret_key


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.token_repository = TokenRepository()

    def validate_login(self, email, password):
        """Validate the login credentials of a user."""
        user = self.user_repository.get_by_email(email)
        if user is None or not check_password_hash(user.password_hash, password):
            return None

        return user

    def generate_access_token(self, user_id, expires_in=10800):
        """Generate a new access token for the user."""
        try:
            payload = {
                "user_id": user_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in),
            }
            new_access_token = jwt.encode(payload, secret_key, algorithm="HS256")
            return new_access_token

        except jwt.PyJWTError as e:
            logging.error(f"JWT Error: {str(e)}")
            raise

        except Exception as e:
            logging.error(f"Error generating access token: {str(e)}")
            raise

    def generate_refresh_token(self, user_id, expires_in=2592000):
        """Generate a new refresh token for the user."""
        try:
            payload = {
                "user_id": user_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in),
            }
            new_refresh_token = jwt.encode(payload, secret_key, algorithm="HS256")
            self.token_repository.save_new_refresh_token(user_id, new_refresh_token)
            return new_refresh_token

        except jwt.PyJWTError as e:
            logging.error(f"JWT Error: {str(e)}")
            raise

        except Exception as e:
            logging.error(f"Error generating access token: {str(e)}")
            raise

    def verify_temp_access_token(self, token):
        """Verify if the provided temporary access token is valid and not expired."""
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                logging.warning("Token missing required field: user_id.")
                return None

            return user_id

        except jwt.ExpiredSignatureError:
            logging.warning("Access token expired.")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Invalid access token.")
            return None
        except Exception as e:
            logging.error(f"Error verifying access token: {str(e)}")
            raise

    def verify_refresh_token(self, token):
        """Verify if the provided refresh token is valid and not expired."""
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                logging.warning("Token missing required field: user_id.")
                return None

            existing_token = self.token_repository.get_token_by_user_id(user_id)
            if not existing_token or existing_token.refresh_token != token:
                return None

            return user_id

        except jwt.ExpiredSignatureError:
            logging.warning("Refresh token expired.")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Invalid refresh token.")
            return None
        except Exception as e:
            logging.error(f"Error verifying refresh token: {str(e)}")
            raise

    def check_email_registered(self, email):
        """Checks if an email is already registered."""
        return self.user_repository.get_by_email(email)

    def save(self, email, password, name, dob, gender, phone_number):
        """Saves a new user to the database."""
        try:
            new_user = self.user_repository.create(
                email, password, name, dob, gender, phone_number
            )
            return new_user

        except Exception as e:
            logging.error(f"Error saving new user: {str(e)}")
            raise

    def generate_verification_code(self, email):
        """Generate a new verification code for the user."""
        try:
            verification_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
            user = self.user_repository.get_by_email(email)
            self.token_repository.save_verification_code(user.id, verification_code)
            return verification_code

        except Exception as e:
            logging.error(f"Error generating verification code: {str(e)}")
            raise

    def generate_confirm_token(self, email, expires_in=3600):
        """Generates a confirmation token for the user."""
        try:
            user_id = self.user_repository.get_by_email(email).id
            payload = {
                "user_id": user_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in),
            }
            new_confirm_token = jwt.encode(payload, secret_key, algorithm="HS256")
            self.token_repository.save_confirm_token(user_id, new_confirm_token)
            return new_confirm_token

        except jwt.PyJWTError as e:
            logging.error(f"JWT Error: {str(e)}")
            raise

        except Exception as e:
            logging.error(f"Error generating confirm token: {str(e)}")
            raise

    def is_verified(self, email):
        """Checks if a user has been verified."""
        user = self.user_repository.get_by_email(email)
        if user and user.is_verified:
            return True

        return False

    def verify_verification_code(self, confirm_token, verification_code):
        """Verifies the confirmation token and verification code."""
        try:
            payload = jwt.decode(confirm_token, secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                logging.warning("Token missing required field: user_id.")
                return None

            token = self.token_repository.get_token_by_user_id(user_id)

            if (
                    token is None
                    or token.confirm_token != confirm_token
                    or token.verification_code != verification_code
                    or token.verification_code_expiration < datetime.now(tz=timezone.utc)
            ):
                return None

            return self.user_repository.get_by_id(user_id)

        except jwt.ExpiredSignatureError:
            logging.warning("Confirm token expired.")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Invalid confirm token.")
            return None
        except Exception as e:
            logging.error(f"Error verifying verification code: {str(e)}")
            raise

    def verify_user_email(self, email):
        """Verifies a user's email."""
        try:
            is_verified = self.user_repository.update_verified_status(email, True)
            if not is_verified:
                return False
            return True

        except Exception as e:
            logging.error(f"Error verifying user email: {str(e)}")
            raise

    def invalidate_refresh_token(self, user_id):
        """Invalidate a user's refresh token."""
        try:
            if self.token_repository.delete_refresh_token(user_id):
                return True
            return False

        except Exception as e:
            logging.error(f"Error invalidating token: {str(e)}")
            raise

    def generate_reset_code(self, email):
        """Generates a reset password code for a user."""
        try:
            reset_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
            user = self.user_repository.get_by_email(email)
            self.token_repository.save_reset_code(user.id, reset_code)
            return reset_code

        except Exception as e:
            logging.error(f"Error generating reset code: {str(e)}")
            raise

    def generate_reset_token(self, email, expires_in=1800):
        """Generates a reset password token for the user."""
        try:
            user_id = self.user_repository.get_by_email(email).id
            payload = {
                "user_id": user_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in),
            }
            new_reset_token = jwt.encode(payload, secret_key, algorithm="HS256")
            self.token_repository.save_reset_token(user_id, new_reset_token)
            return new_reset_token

        except jwt.PyJWTError as e:
            logging.error(f"JWT Error: {str(e)}")
            raise

        except Exception as e:
            logging.error(f"Error generating reset token: {str(e)}")
            raise

    def verify_reset_code(self, reset_token, reset_code):
        """Verifies the reset password token and reset password code."""
        try:
            payload = jwt.decode(reset_token, secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                logging.warning("Token missing required field: user_id.")
                return None

            token = self.token_repository.get_token_by_user_id(user_id)
            if (
                    token is None
                    or token.reset_token != reset_token
                    or token.reset_code != reset_code
                    or token.reset_code_expiration < datetime.now(tz=timezone.utc)
            ):
                return None

            return self.user_repository.get_by_id(user_id)

        except jwt.ExpiredSignatureError:
            logging.warning("Reset token expired.")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Invalid reset token.")
            return None
        except Exception as e:
            logging.error(f"Error verifying reset code: {str(e)}")
            raise

    def set_password(self, user_id, new_password):
        """Set a new password for the user."""
        try:
            user = self.user_repository.get_by_id(user_id)
            if user is None:
                return False

            self.user_repository.update_password(user, new_password)
            return True

        except Exception as e:
            logging.error(f"Error setting password: {str(e)}")
            raise
