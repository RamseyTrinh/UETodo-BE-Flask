import logging

from app.repository import TaskRepository

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def get_task_by_id(self, task_id):
        try:
            return self.task_repository.get_by_id(task_id)
        except Exception as e:
            logging.error(f"Error retrieving task by ID: {str(e)}")
            raise

    def create_task(self, name, description, status, due_date, priority, user_id):
        try:
            return self.task_repository.create(
                name=name,
                description=description,
                status=status,
                due_date=due_date,
                priority=priority,
                user_id=user_id
            )
        except Exception as e:
            logging.error(f"Error creating task: {str(e)}")
            raise

    def update_task(self, task_id, data):
        try:
            return self.task_repository.update(task_id, data)
        except Exception as e:
            logging.error(f"Error updating task: {str(e)}")
            raise
    
    def delete_task(self, task_id):
        try:
            return self.task_repository.delete(task_id)
        except Exception as e:
            logging.error(f"Error deleting task: {str(e)}")
            raise
        
    def get_list_tasks(self, page=1, per_page=10):
        try:
            return self.task_repository.get_list(page, per_page)
        except Exception as e:
            logging.error(f"Error retrieving task list: {str(e)}")
            raise