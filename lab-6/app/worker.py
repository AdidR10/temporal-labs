# worker/worker.py
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from cronWorkflow import CronWorkflow

async def main():
    import os
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")
    client = await Client.connect(temporal_address)
    
    worker = Worker(
        client,
        task_queue="lab6-queue",
        workflows=[CronWorkflow],
    )
    
    print("Worker started")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())