import asyncio
from temporalio.client import Client # type: ignore
from temporalio.worker import Worker # type: ignore
from hello_workflow import HelloWorkflow
from hello_activity import say_hello

async def main():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Create a worker that listens to a task queue
    worker = Worker(
        client,
        task_queue="hello-task-queue",
        workflows=[HelloWorkflow],
        activities=[say_hello],
    )
    
    # Run the worker
    print("Starting worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main()) 