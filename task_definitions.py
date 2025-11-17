from conductor.client.http.models import TaskDef

def get_task_definitions():
    
    task_def = TaskDef()
    task_def.name = 'insertUserData_1'
    task_def.retry_count = 3,
    task_def.retry_logic = 'FIXED'
    task_def.retry_delay_seconds = 60
    
    return task_def
