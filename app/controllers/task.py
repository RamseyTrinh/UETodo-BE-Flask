from flask import request
from flask_restx import Resource

from app.schemas import TaskSchema
from app.services import TaskService

task_api = TaskSchema.api

@task_api.route("")
class TaskController(Resource):
    @task_api.doc("Create a new task")
    @task_api.expect(TaskSchema.create_task_model, validate=True)
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400
        service = TaskService()
        task = service.create_task(data)
        return {"success": True, "data": task.as_dict()}, 201
    
    @task_api.doc("Get all tasks")
    @task_api.param("page", "Page number", type=int, default=1)
    @task_api.param("per_page", "Items per page", type=int, default=10)
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        service = TaskService()
        tasks = service.get_list_tasks(page, per_page)
        result_tasks = [task.as_dict() for task in tasks]
        return {"success": True, "data": result_tasks}, 200
    
@task_api.route("/<int:id>")
@task_api.param("id", "Task ID")
class TaskItemController(Resource):
    @task_api.doc("Get task by ID")
    def get(self, id):
        service = TaskService()
        task = service.get_task_by_id(id)
        if task:
            return {"success": True, "data": task.as_dict()}, 200
        return {"success": False, "message": "Task not found"}, 404
    
    @task_api.expect(TaskSchema.update_task_model, validate=True)
    def put(self, id):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "Invalid JSON data."}, 400
        service = TaskService()
        updated_task = service.update_task(id, data)
        return {"success": True, "data": updated_task.as_dict()}, 200
    
    def delete(self, id):
        service = TaskService()
        service.delete_task(id)
        return {"success": True, "message": "Task deleted successfully."}, 204
    