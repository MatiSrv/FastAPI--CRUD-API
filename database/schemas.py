def individual_data(todo):
    return{
        "id": str(todo["_id"]),
        "title": str(todo["title"]),
        "description": str(todo["description"]),
        "status": str(todo["is_completed"]),
    }
    
def all_data(todos):
    return [individual_data(todo) for todo in todos]