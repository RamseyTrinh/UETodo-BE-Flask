import logging

from werkzeug.security import generate_password_hash

from .. import db
from ..models.user import User as UserModel


class UserRepository:
    @staticmethod
    def get_by_id(user_id) -> UserModel:
        return db.session.execute(
            db.select(UserModel).where(UserModel.id == user_id)
        ).scalar()

    @staticmethod
    def get_by_email(email) -> UserModel:
        return db.session.execute(
            db.select(UserModel).where(UserModel.email == email)
        ).scalar()

    @staticmethod
    def create(
            email, password, name, dob, gender, phone_number
    ) -> UserModel:
        try:
            new_user = UserModel(
                email=email,
                password=password,
                name=name,
                dob=dob,
                gender=gender,
                phone_number=phone_number,
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating new user: {str(e)}")
            raise

    def update_verified_status(self, email, status) -> bool:
        try:
            user = self.get_by_email(email)
            if not user:
                return False

            user.is_verified = status
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating user verified status: {str(e)}")
            raise

    @staticmethod
    def update_password(user, new_password):
        try:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            return user

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating user password: {str(e)}")
            raise

    @staticmethod
    def update(user_id: int, data: dict) -> UserModel:
        try:
            user = db.session.get(UserModel, user_id)
            if not user:
                raise ValueError("User not found")

            for field in [
                "email",
                "name",
                "gender",
                "phone_number",
                "avatar_url",
                "is_verified",
            ]:
                if field in data:
                    setattr(user, field, data[field])

            db.session.commit()
            return user

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating user {user_id}: {str(e)}")
            raise

    def delete(self, user_id: int) -> bool:
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False

            db.session.delete(user)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting user: {str(e)}")
            raise

    @staticmethod
    def get_list(
            page: int = 1, per_page: int = 10
    ) -> list[UserModel]:
        
        stmt = (
            db.select(UserModel)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )        
        result = db.session.execute(stmt).scalars().all()
        return result
