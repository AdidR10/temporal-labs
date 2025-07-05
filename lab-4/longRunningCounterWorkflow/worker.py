import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Import the workflow
from counter_workflow import CounterWorkflow

async def main():
    """Worker that processes long-running counter workflows."""
    
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Create worker with counter workflow
    worker = Worker(
        client,
        task_queue="long-running-counter-task-queue",
        workflows=[CounterWorkflow],
    )
    
    print("🔄 Long-running Counter Worker started!")
    print("📋 Listening on task queue: long-running-counter-task-queue")
    print("🎯 Ready to process counter workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())