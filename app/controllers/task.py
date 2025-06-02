from flask import request
from flask_restx import Resource

from app.schemas import TaskSchema
from app.services import TaskService

from datetime import datetime, timedelta

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
    
def serialize_task(task):
        return {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "created_at": task.created_at.isoformat(),
            "start_date": task.start_date.isoformat() if task.start_date else None,
            "due_date": task.due_date.isoformat() if task.due_date else None,
        }
@task_api.route("/user/<int:user_id>")
@task_api.param("user_id", "User ID")
@task_api.param("page", "Page number", type=int, default=1)
@task_api.param("per_page", "Items per page", type=int, default=10)
class UserTasksController(Resource):
    
    @task_api.doc("Get tasks by user ID")
    def get(self, user_id):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        service = TaskService()
        tasks = service.get_tasks_by_user_id(user_id, page, per_page)
        result_tasks = [serialize_task(task) for task in tasks]
        return {"success": True, "data": result_tasks}, 200
    
@task_api.route("/dashboard/<user_id>")
@task_api.param("user_id", "User ID")
class DashboardTasksController(Resource):
    @task_api.doc("Get dashboard tasks by user ID")
    def get(self, user_id):
        service = TaskService()
        tasks = service.get_tasks_by_user_id(user_id, 1, 10000)
        
        today = datetime.utcnow().date()
        
        completed_tasks = [task for task in tasks if task.status == True]
        overdue_tasks = [task for task in tasks if task.due_date and task.due_date.date() < today and not task.status]
        
        total_tasks = len(tasks)
        total_overdue_tasks = len(overdue_tasks)
        total_completed_tasks = len(completed_tasks)
        total_remaining_tasks = total_tasks - total_completed_tasks
        
        result_tasks = {
            "total_task": total_tasks,
            "total_overdue_tasks": total_overdue_tasks,
            "total_completed_tasks": total_completed_tasks,
            "total_remaining_tasks": total_remaining_tasks,
        }
        
        return {"success": True, "data": result_tasks}, 200
    
@task_api.route("/dashboard/barchart/<user_id>")
@task_api.param("user_id", "User ID")
class DashboardTasksController(Resource):
    @task_api.doc("Get barchart tasks by user ID")
    def get(self, user_id):
        service = TaskService()
        tasks = service.get_tasks_by_user_id(user_id, 1, 10000)
        
        today = datetime.utcnow().date()
        
        completed_tasks = [task for task in tasks if task.status is True]
        overdue_tasks = [
            task for task in tasks
            if task.due_date and task.due_date.date() < today and not task.status
        ]
        
        # --- Thống kê theo priority ---
        priorities = ["Low", "Medium", "High"]

        def count_by_priority(task_list):
            result = {p: 0 for p in priorities}
            for task in task_list:
                if task.priority in result:
                    result[task.priority] += 1
            return [result[p] for p in priorities]

        priority_overdue = count_by_priority(overdue_tasks)
        priority_completed = count_by_priority(completed_tasks)

        result_tasks = {
            "categories": priorities,
            "overdue": priority_overdue,
            "completed": priority_completed
        }

        return {"success": True, "data": result_tasks}, 200

@task_api.route("/dashboard/linechart/<user_id>")
@task_api.param("user_id", "User ID")
class UserActivityController(Resource):
    @task_api.doc("Get task created activity by user ID")
    def get(self, user_id):
        service = TaskService()
        tasks = service.get_tasks_by_user_id(user_id, 1, 10000)

        today = datetime.utcnow().date()
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]

        task_counts_by_day = {day: 0 for day in days}

        for task in tasks:
            created_date = task.start_date.date() if task.start_date else None
            if created_date in task_counts_by_day:
                task_counts_by_day[created_date] += 1

        result = {
            "days": [day.strftime("%a") for day in days],
            "counts": [task_counts_by_day[day] for day in days],
        }

        return {"success": True, "data": result}, 200
    
@task_api.route("/dashboard/overview/<user_id>")
@task_api.param("user_id", "User ID")
class DashboardRecentTasksController(Resource):
    @task_api.doc("Get recent completed and upcoming tasks")
    def get(self, user_id):
        service = TaskService()
        tasks = service.get_tasks_by_user_id(user_id, 1, 10000)

        today = datetime.utcnow().date()
        completed_tasks = [
            {
                "name": task.name,
                "description": task.description,
                "priority": task.priority,
                "start_date": task.start_date.strftime("%d-%m-%Y") if task.start_date else None,
                "completed_date": task.updated_at.strftime("%d-%m-%Y") if task.updated_at else None,
            }
            for task in tasks if task.status == True
        ]

        upcoming_tasks = [
            {
                "name": task.name,
                "description": task.description,
                "priority": task.priority,
                "start_date": task.start_date.strftime("%d-%m-%Y") if task.start_date else None,
                "due_date": task.due_date.strftime("%d-%m-%Y") if task.due_date else None,
            }
            for task in tasks if task.status == False and task.due_date and task.due_date.date() >= today
        ]

        return {
            "success": True,
            "data": {
                "completed": completed_tasks,
                "upcoming": upcoming_tasks
            }
        }, 200
