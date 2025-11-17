from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.configuration.configuration import AuthenticationSettings
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.orkes_clients import OrkesClients
from conductor.client.http.models import TaskDef
from workflow import new_user_onboarding_workflow
from workflow_input import WorkflowInput
from task_definitions import get_task_definitions

SERVER_URL = 'https://adrian-demo.orkesconductor.io/api'
KEY = 'a735202c-c1c1-11f0-bca6-2ece4f2789ea'	
SECRET = '5HcN3owzY5kiqCQ7BPzrGKbUveO3RMTTRbLt5iOstOgaw871' 

def register_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = new_user_onboarding_workflow(workflow_executor=workflow_executor)
    workflow.register(True)
    return workflow


def main():
    
    api_config = Configuration(
      server_api_url=SERVER_URL,
      authentication_settings=AuthenticationSettings(
         key_id=KEY,
         key_secret=SECRET
      ),
    )

    workflow_executor = WorkflowExecutor(configuration=api_config)

    workflow = register_workflow(workflow_executor)

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    input_data = WorkflowInput("sample@email.com", "silver")
    workflow_run = workflow_executor.execute(
        name=workflow.name,
        version=workflow.version,
        workflow_input=input_data.to_dict()
    )

    print(f'\nworkflow result: {workflow_run.output}\n')
    print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_run.workflow_id}\n')

    #task_handler.stop_processes()

if __name__ == '__main__':
    main()
