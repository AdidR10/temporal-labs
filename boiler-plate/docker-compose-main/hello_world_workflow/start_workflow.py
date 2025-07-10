import asyncio
from temporalio.client import Client
from hello_workflow import HelloWorkflow

async def main():
    """
    Script to start a workflow programmatically.
    """
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Execute workflow and wait for result
    result = await client.execute_workflow(
        HelloWorkflow.run,
        "World",
        id="hello-workflow-id",
        task_queue="hello-task-queue",
    )
    
    print(f"✅ Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())