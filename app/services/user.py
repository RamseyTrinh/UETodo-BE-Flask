import logging

from app.repository import UserRepository
from werkzeug.security import check_password_hash, generate_password_hash


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_list_menu(self, page=1, per_page=10):
        try:
            return self.user_repository.get_list(page, per_page)
        except Exception as e:
            logging.error(f"Error retrieving user list: {str(e)}")
            raise

    def get_user_by_id(self, user_id):
        try:
            return self.user_repository.get_by_id(user_id)
        except Exception as e:
            logging.error(f"Error retrieving user by ID: {str(e)}")
            raise

    def update_password(self, user_id, old_password, new_password):
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            if not old_password:
                raise ValueError("Old password cannot be empty")
            
            if not check_password_hash(user.password_hash, old_password):
                raise ValueError("Old password is incorrect")

            if not new_password:
                raise ValueError("New password cannot be empty")
            
            if old_password == new_password:
                raise ValueError("New password cannot be the same as old password")
            
            return self.user_repository.update_password(user, new_password)
        except Exception as e:
            logging.error(f"Error updating password: {str(e)}")
            raise

    def update_user(self, user_id, user):
        try:
            return self.user_repository.update(user_id, user)
        except Exception as e:
            logging.error(f"Error updating user: {str(e)}")
            raise

    def delete_user(self, user_id):
        try:
            return self.user_repository.delete(user_id)
        except Exception as e:
            logging.error(f"Error deleting menu: {str(e)}")
            raise
        
    def new_password(self, email, new_password):
        try:
            user = self.user_repository.get_by_email(email)
            if not user:
                raise ValueError("User not found")
            
            if not new_password:
                raise ValueError("New password cannot be empty")
            
            return self.user_repository.update_password(user, new_password)
        except Exception as e:
            logging.error(f"Error updating password: {str(e)}")
            raise
