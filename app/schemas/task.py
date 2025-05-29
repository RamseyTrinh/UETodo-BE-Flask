from flask_restx import Namespace, fields, reqparse

class TaskSchema:
    api = Namespace("task", description="Task related operations")
    
    create_task_model = api.model(
        "CreateTask",
        {
            "name": fields.String(required=True, description="Title of the task"),
            "description": fields.String(required=True, description="Description of the task"),
            "start_date": fields.String(required=True, description="Start date of the task in YYYY-MM-DD format"),
            "due_date": fields.String(required=True, description="Due date of the task in YYYY-MM-DD format"),
            "priority": fields.String(required=True, description="Priority of the task"),
            "user_id": fields.Integer(required=True, description="ID of the user who owns the task"),
        },
    )
    
    update_task_model = api.model(
        "UpdateTask",
        {
            "name": fields.String(description="Title of the task"),
            "description": fields.String(description="Description of the task"),
            "start_date": fields.String(description="Start date of the task in YYYY-MM-DD format"),
            "due_date": fields.String(description="Due date of the task in YYYY-MM-DD format"),
            "priority": fields.String(description="Priority of the task"),
            "status": fields.Boolean(description="Status of the task"),
        },
    )
    