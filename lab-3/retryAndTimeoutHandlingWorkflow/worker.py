import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from greeting_workflow import RetryAndTimeoutWorkflow
from compose_greeting_activity import unreliable_greeting_activity, slow_processing_activity

async def main():
    """Worker that processes retry and timeout demonstration workflows."""
    
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Create worker with all our workflows and activities
    worker = Worker(
        client,
        task_queue="retry-timeout-task-queue",
        workflows=[RetryAndTimeoutWorkflow],
        activities=[unreliable_greeting_activity, slow_processing_activity],
    )
    
    print("🔄 Retry and Timeout Worker started!")
    print("📋 Listening on task queue: retry-timeout-task-queue")
    print("🎯 Ready to demonstrate failure handling...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())