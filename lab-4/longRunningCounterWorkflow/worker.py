import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Import the workflow and activity
from counter_workflow import CounterWorkflow

async def main():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Create a worker that listens to a task queue
    worker = Worker(
        client,
        task_queue="long-running-counter-task-queue",
        workflows=[CounterWorkflow],
    )
    
    print("Starting worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())