import asyncio
from temporalio.client import Client # type: ignore
from hello_workflow import GreetingWorkflow

async def main():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Start the workflow
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "Worlddddd!",
        id="hello-activity-retry-workflow-id",
        task_queue="hello-activity-retry-task-queue",
    )
    print(f"Result: {result}")
    
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())