import logging
from datetime import datetime, timezone, timedelta

from .. import db
from ..models.token import Token as TokenModel


class TokenRepository:
    @staticmethod
    def get_token_by_user_id(user_id) -> TokenModel:
        return db.session.execute(
            db.select(TokenModel).where(TokenModel.user_id == user_id)
        ).scalar()

    @staticmethod
    def save_new_refresh_token(user_id, new_refresh_token):
        try:
            existing_token = db.session.execute(
                db.select(TokenModel).where(TokenModel.user_id == user_id)
            ).scalar()

            if not existing_token:
                new_token = TokenModel(user_id=user_id, refresh_token=new_refresh_token)
                db.session.add(new_token)
            else:
                existing_token.refresh_token = new_refresh_token

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving new refresh token: {str(e)}")
            raise

    @staticmethod
    def save_verification_code(user_id, code):
        try:
            token = db.session.execute(
                db.select(TokenModel).where(TokenModel.user_id == user_id)
            ).scalar()

            if not token:
                new_token = TokenModel(
                    user_id=user_id,
                    verification_code=code,
                    verification_code_expiration=datetime.now(tz=timezone.utc)
                                                 + timedelta(hours=10),
                )
                db.session.add(new_token)
            else:
                token.verification_code = code
                token.verification_code_expiration = datetime.now(
                    tz=timezone.utc
                ) + timedelta(minutes=10)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving verification code: {str(e)}")
            raise

    @staticmethod
    def save_reset_code(user_id, code):
        try:
            token = db.session.execute(
                db.select(TokenModel).where(TokenModel.user_id == user_id)
            ).scalar()

            if not token:
                new_token = TokenModel(
                    user_id=user_id,
                    reset_code=code,
                    reset_code_expiration=datetime.now(tz=timezone.utc)
                                          + timedelta(hours=10),
                )
                db.session.add(new_token)
            else:
                token.reset_code = code
                token.reset_code_expiration = datetime.now(tz=timezone.utc) + timedelta(
                    hours=10
                )

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving reset code: {str(e)}")
            raise

    @staticmethod
    def save_confirm_token(user_id, token):
        try:
            existing_token = db.session.execute(
                db.select(TokenModel).where(TokenModel.user_id == user_id)
            ).scalar()

            if not existing_token:
                new_token = TokenModel(user_id=user_id, confirm_token=token)
                db.session.add(new_token)
            else:
                existing_token.confirm_token = token

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving confirm token: {str(e)}")
            raise

    @staticmethod
    def save_reset_token(user_id, token):
        try:
            existing_token = db.session.execute(
                db.select(TokenModel).where(TokenModel.user_id == user_id)
            ).scalar()

            if not existing_token:
                new_token = TokenModel(user_id=user_id, reset_token=token)
                db.session.add(new_token)
            else:
                existing_token.reset_token = token

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving reset token: {str(e)}")
            raise

    def delete_refresh_token(self, user_id):
        try:
            token = self.get_token_by_user_id(user_id)
            if not token:
                return False

            token.refresh_token = None
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting refresh token: {str(e)}")
            raise
