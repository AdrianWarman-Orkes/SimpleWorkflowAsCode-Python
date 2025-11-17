from conductor.client.worker.worker_task import worker_task
from conductor.client.worker.worker import TaskResult
from conductor.client.http.models.task_result_status import TaskResultStatus

@worker_task(task_definition_name='insertUserData')
def insert_user_data(email: str, planType: str) -> TaskResult:
    result = TaskResult()
    result.log("Inserting user now...")

    result.add_output_data(
        "statusMessage", f"User {email} has been inserted with planType {planType}"
    )
    
    result.status = TaskResultStatus.COMPLETED

    return result
