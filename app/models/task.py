
from datetime import datetime
from flask_pymongo import ObjectId
from app.factory import mongo


class Task:
    def __init__(self, title, intensity, status, deadline):
        self.title = title
        self.intensity = intensity
        self.status = status
        self.deadline = deadline

    def save(self):
        task_data = {
            "title": self.title,
            "intensity": self.intensity,
            "status": self.status,
            "deadline": self.deadline
        }
        result = mongo.db.tasks.insert_one(task_data)
        return result.inserted_id

    @staticmethod
    def find_all():
        return mongo.db.tasks.find()

    @staticmethod
    def find_by_id(task_id):
        return mongo.db.tasks.find_one({"_id": ObjectId(task_id)})

    @staticmethod
    def update(task_id, title=None, intensity=None, status=None, deadline=None):
        update_data = {}
        if title:
            update_data["title"] = title
        if intensity:
            update_data["intensity"] = intensity
        if status:
            update_data["status"] = status
        if deadline:
            update_data["deadline"] = deadline

        result = mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)}, {"$set": update_data})
        return result.modified_count

    @staticmethod
    def delete(task_id):
        result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count
