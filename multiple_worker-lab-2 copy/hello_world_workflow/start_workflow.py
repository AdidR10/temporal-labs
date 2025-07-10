import asyncio
import sys
from temporalio.client import Client
from hello_workflow import HelloWorkflow

async def main(workflow_id=None):
    """
    Script to start a workflow programmatically.
    """
    # Use provided workflow_id or default
    if workflow_id is None:
        workflow_id = "hello-workflow-id"
    
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Execute workflow and wait for result
    result = await client.execute_workflow(
        HelloWorkflow.run,
        "World",
        id=workflow_id,
        task_queue="hello-task-queue",
    )
    
    print(f"✅ Workflow result: {result}")

if __name__ == "__main__":
    # Get workflow ID from command line argument if provided
    workflow_id_arg = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(workflow_id_arg))