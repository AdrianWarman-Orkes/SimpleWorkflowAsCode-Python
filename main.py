from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.configuration import AuthenticationSettings
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.orkes_clients import OrkesClients
from conductor.client.http.models import TaskDef
from workflow import new_user_onboarding_workflow
from workflow_input import WorkflowInput
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")


def register_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = new_user_onboarding_workflow(workflow_executor=workflow_executor)
    workflow.register(True)
    return workflow

def get_task_definition():
    
    task_def = TaskDef()
    task_def.name = 'insertUserData_1'
    task_def.retry_count = 3,
    task_def.retry_logic = 'FIXED'
    task_def.retry_delay_seconds = 60
    
    return task_def



def main():
    
    api_config = Configuration(
      server_api_url=SERVER_URL,
      authentication_settings=AuthenticationSettings(
         key_id=KEY,
         key_secret=SECRET
      ),
    )

    workflow_executor = WorkflowExecutor(configuration=api_config)

    clients = OrkesClients(configuration=api_config)

    metadata_client = clients.get_metadata_client()

    metadata_client.register_task_def(task_def=get_task_definition())

    workflow = register_workflow(workflow_executor)

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    input_data = WorkflowInput("sample@email.com", "silver")
    workflow_run = workflow_executor.execute(
        name=workflow.name,
        version=workflow.version,
        workflow_input=input_data.to_dict()
    )

    print(f'\nworkflow result: {workflow_run.output["result"]}\n')
    print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_run.workflow_id}\n')

    #task_handler.stop_processes()

if __name__ == '__main__':
    main()
