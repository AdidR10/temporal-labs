import asyncio
from temporalio.client import Client # type: ignore
from parent_and_child_workflow import ParentWorkflow

async def main():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Start the workflow

    result = await client.execute_workflow(
        ParentWorkflow.run,
        [1, 2],
        id="parent-and-child-workflow-id",
        task_queue="parent-and-child-task-queue",
    )
    print(result)
    print(f"Workflow execution completed!")

if __name__ == "__main__":
    asyncio.run(main())