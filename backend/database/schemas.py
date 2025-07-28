def individual_data(todo):
    if not todo["is_deleted"]:
        return {
            "id": str(todo["_id"]),
            "name": todo["title"],
            "description": todo["description"],
            "status": todo["is_completed"],
            "created_on": todo["created_on"]
        }
    return None  

def all_tasks(todos):
    return [data for todo in todos if (data := individual_data(todo)) is not None]
