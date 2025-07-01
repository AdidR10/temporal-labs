import os
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from CronWorkflow import CronWorkflow
from activity import say_hello

async def connect_with_retry(address: str, max_retries: int = 10, delay: int = 5):
    """Connect to Temporal with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"Worker: Attempting to connect to Temporal at {address} (attempt {attempt + 1}/{max_retries})")
            client = await Client.connect(address)
            print("Worker: Successfully connected to Temporal!")
            return client
        except Exception as e:
            print(f"Worker: Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Worker: Waiting {delay} seconds before retrying...")
                await asyncio.sleep(delay)
            else:
                raise

async def main():
    # Connect to Temporal server
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    client = await connect_with_retry(temporal_address)
    
    # Create worker
    task_queue = os.getenv("TASK_QUEUE", "cron-task-queue")
    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[CronWorkflow],
        activities=[say_hello],
    )
    
    print(f"Worker: Starting worker on task queue: {task_queue}")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 