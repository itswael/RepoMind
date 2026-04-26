def validate_task(task):
    if task["confidence"] < 0.6:
        return False
    
    if len(task["task"].split()) < 3:
        return False
    
    return True