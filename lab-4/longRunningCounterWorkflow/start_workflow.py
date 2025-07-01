import asyncio
from temporalio.client import Client # type: ignore
from counter_workflow import CounterWorkflow

async def main():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Start the workflow
    await client.execute_workflow(
        CounterWorkflow.run,
        id="long-running-counter-workflow-id",
        task_queue="long-running-counter-task-queue",
    )
    
    print(f"Workflow execution completed!")

if __name__ == "__main__":
    asyncio.run(main())