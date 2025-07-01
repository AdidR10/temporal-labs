import asyncio
from temporalio.client import Client # type: ignore
from temporalio.worker import Worker # type: ignore
from greeting_workflow import GreetingWorkflow
from compose_greeting_activity import compose_greeting

async def main():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Create a worker that listens to a task queue
    worker = Worker(
        client,
        task_queue="hello-activity-retry-task-queue",
        workflows=[GreetingWorkflow],
        activities=[compose_greeting]
    )
    
    # Run the worker
    print("Starting worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 