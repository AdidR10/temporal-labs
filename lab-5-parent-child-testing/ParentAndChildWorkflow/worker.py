import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Import both parent and child workflows
from parent_and_child_workflow import ParentWorkflow, ChildWorkflow, NestedChildWorkflow

async def main():
    """Worker that processes both parent and child workflows."""
    
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Create worker with both workflow types
    worker = Worker(
        client,
        task_queue="parent-and-child-task-queue",
        workflows=[ParentWorkflow, ChildWorkflow, NestedChildWorkflow],  # Register both workflow types
    )
    
    print("🔄 Parent-Child Workflow Worker started!")
    print("📋 Listening on task queue: parent-and-child-task-queue")
    print("🎯 Ready to process parent and child workflows...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())