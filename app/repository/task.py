import logging

from .. import db
from ..models.task import Task as TaskModel


class TaskRepository:
    @staticmethod
    def get_by_id(task_id) -> TaskModel:
        return db.session.execute(
            db.select(TaskModel).where(TaskModel.id == task_id)
        ).scalar()

    @staticmethod
    def create(
            name, description, start_date, due_date, priority, user_id
    ) -> TaskModel:
        try:
            new_task = TaskModel(
                name=name,
                description=description,
                start_date=start_date,
                due_date=due_date,
                priority=priority,
                user_id=user_id,
            )
            db.session.add(new_task)
            db.session.commit()
            return new_task

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating new task: {str(e)}")
            raise

    @staticmethod
    def update(task_id: int, data: dict) -> TaskModel:
        try:
            task = db.session.get(TaskModel, task_id)
            if not task:
                raise ValueError("Task not found")

            for field in [
                "name",
                "description",
                "status",
                "start_date",
                "due_date",
                "priority",
                "user_id",
            ]:
                if field in data:
                    setattr(task, field, data[field])

            db.session.commit()
            return task

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating task {task_id}: {str(e)}")
            raise

    def delete(self, task_id: int) -> bool:
        try:
            task = self.get_by_id(task_id)
            if not task:
                return False

            db.session.delete(task)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting task: {str(e)}")
            raise

    @staticmethod
    def get_list(
            page: int = 1, per_page: int = 10
    ) -> list[TaskModel]:
            stmt = (
                db.select(TaskModel)
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            result = db.session.execute(stmt).scalars().all()
            return result
        
    @staticmethod
    def get_list_by_user_id(user_id: int, page: int = 1, per_page: int = 10) -> list[TaskModel]:
        stmt = (
            db.select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        result = db.session.execute(stmt).scalars().all()
        return result
