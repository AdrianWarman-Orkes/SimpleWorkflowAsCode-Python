from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.javascript_task import JavascriptTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.http_task import HttpTask, HttpInput, HttpMethod
from conductor.client.workflow.task.terminate_task import TerminateTask, WorkflowStatus
from worker import insert_user_data 

def new_user_onboarding_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    name = 'newUserOnboarding_python'
    workflow = ConductorWorkflow(name=name, executor=workflow_executor, description="simple workflow to onboard new users")
    workflow.version = 1

    validation_script = """
        (function () {
        const emailFormat = /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/;
        const validPlans = ["bronze", "silver", "gold"];

        if (!$.email || !emailFormat.test($.email)) {
            return {
            valid: false,
            message: "Invalid or missing email"
            };
        }

        if (!$.planType || !validPlans.includes($.planType)) {
            return {
            valid: false,
            message: "Invalid or missing planType. Must be bronze, silver, or gold"
            };
        }

        return {
            valid: true,
            message: "Validated user"
        };
        })();
        """
    
    inline_task = JavascriptTask(
        task_ref_name="validate_user_data_ref",
        script=validation_script,
        bindings={'email': '${workflow.input.email}', 'planType': '${workflow.input.planType}'}
    )
    inline_task.name = "validate_user_data"

    workflow >> inline_task


    http_task = HttpTask(
        task_ref_name="notify_and_try_again_ref",
        http_input= HttpInput(
            method=HttpMethod.POST,
            uri="https://orkes-api-tester.orkesconductor.com/api",
            headers={"Content-Type": ["application/json"]},
            body={
                "valid": False,
                "message": "${validate_user_data_ref.output.result.message}"
            }
        )
    )
    http_task.name = "notify_and_try_again"

    terminate_task = TerminateTask(
        task_ref_name="terminate_ref",
        status=WorkflowStatus.TERMINATED,
        termination_reason="${validate_user_data_ref.output.result.message}"
    )
    terminate_task.name = "terminate"


    switch_task = SwitchTask(
        task_ref_name="switch_ref",
        case_expression="${validate_user_data_ref.output.result.valid}",
        use_javascript=False
    )
    switch_task.switch_case(case_name="true", tasks=[])
    switch_task.switch_case(case_name="false", tasks=[http_task, terminate_task])
    SwitchTask.name = "switch"

    workflow >> switch_task

    simple_task = insert_user_data(
        task_ref_name='insertUserData', 
        email=workflow.input('email'), 
        planType=workflow.input('planType'))

    workflow >> simple_task

    return workflow
