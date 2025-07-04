import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from hello_workflow import HelloWorkflow
from hello_activity import say_hello

async def main():
    """
    Worker connects to Temporal server and processes workflows/activities.
    """
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Create worker that listens to task queue
    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[HelloWorkflow],  # Register workflow
        activities=[say_hello],     # Register activity
    )
    
    print("🚀 Worker started! Listening for workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())