from flask import request
from flask_restx import Resource

from app.schemas import UserSchema
from app.services import UserService
from app.utils.decorators import JWT_required

user_api = UserSchema.api


@user_api.route("")
class UserController(Resource):
    @user_api.doc("Get all menu")
    @user_api.param("page", "Page number", type=int, default=1)
    @user_api.param("per_page", "Items per page", type=int, default=10)
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 1000, type=int)
        
        service = UserService()
        items = service.get_list_menu(page, per_page)
        result_items = [item.as_dict() for item in items]
        return {"success": True, "data": result_items}, 200


@user_api.route("/me")
class CurrentUserController(Resource):
    @JWT_required
    @user_api.doc(security='Bearer Auth')
    def get(self, user=None):
        return {
            "success": True,
            "message": "User retrieved successfully.",
            "user": user.as_dict(),
        }, 200


@user_api.route("/<int:id>")
@user_api.param("id", "")
class UserItemController(Resource):
    @user_api.doc("Get user by ID")
    def get(self, id):
        service = UserService()
        item = service.get_user_by_id(id)
        if item:
            return {"success": True, "data": item.as_dict()}, 200
        return {"success": False, "message": "User not found"}, 404

    @user_api.expect(UserSchema.user_model, validate=True)
    def put(self, id):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400
        service = UserService()
        updated = service.update_user(id, data)
        if updated:
            return {
                "success": True,
                "message": "User updated",
            }, 200
        return {"success": False, "message": "Update failed or user not found"}, 400

    @JWT_required
    def delete(self, id):
        service = UserService()
        deleted = service.delete_user(id)
        if deleted:
            return {"success": True, "message": "User deleted"}, 200
        return {"success": False, "message": "Delete failed or user not found"}, 400

    @user_api.route("/<int:id>/password")
    @user_api.param("id", "User ID")
    class UserPasswordController(Resource):
        @user_api.expect(UserSchema.password_update_model, validate=True)
        def put(self, id):
            data = request.get_json()
            if not data or "new_password" not in data:
                return {"success": False, "message": "Missing 'new_password'"}, 400
            if "old_password" not in data:
                return {"success": False, "message": "Missing 'old_password'"}, 400

            old_password = data["old_password"]
            new_password = data["new_password"]

            service = UserService()
            try:
                updated = service.update_password(id, old_password, new_password)
                return {"success": True, "message": "Password updated successfully"}, 200
            except ValueError as e:
                return {"success": False, "message": str(e)}, 400
            except Exception:
                return {"success": False, "message": "Internal server error"}, 500
            
@user_api.route("/update-new-password")
class NewPasswordController(Resource):
    @user_api.expect(UserSchema.new_password_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400

        email = data.get("email")
        new_password = data.get("new_password")
        if not new_password or not email:
            return {
                "success": False,
                "message": "New password and email are required.",
            }, 400

        service = UserService()
        service.new_password(email, new_password)
        return {"success": True, "message": "Password updated successfully."}, 200
