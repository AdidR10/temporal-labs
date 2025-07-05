import asyncio
from temporalio.client import Client
from greeting_workflow import RetryAndTimeoutWorkflow

async def run_scenario(client: Client, scenario: str, name: str):
    """Run a specific failure handling scenario."""
    
    workflow_id = f"retry-timeout-{scenario}-{name}"
    
    print(f"\n🚀 Starting {scenario} scenario for {name}")
    print(f"📋 Workflow ID: {workflow_id}")
    
    try:
        result = await client.execute_workflow(
            RetryAndTimeoutWorkflow.run,
            args=[name, scenario],
            id=workflow_id,
            task_queue="retry-timeout-task-queue",
        )
        print(f"✅ {scenario} result: {result}")
        return result
        
    except Exception as e:
        print(f"❌ {scenario} failed: {e}")
        return str(e)

async def main():
    """Demonstrate different retry and timeout scenarios."""
    
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    print("🎯 Retry and Timeout Handling Demonstrations")
    print("=" * 50)
    
    # Scenario 1: Retry demonstration
    await run_scenario(client, "retry_demo", "Alice")
    
    # Wait a bit between scenarios
    await asyncio.sleep(2)
    
    # Scenario 2: Timeout demonstration  
    await run_scenario(client, "timeout_demo", "Bob")
    
    # Wait a bit between scenarios
    await asyncio.sleep(2)
    
    # Scenario 3: Heartbeat demonstration
    await run_scenario(client, "heartbeat_demo", "Charlie")
    
    # Wait a bit between scenarios
    await asyncio.sleep(2)
    
    # Scenario 4: Comprehensive demonstration
    await run_scenario(client, "comprehensive_demo", "Demo")
    
    print("\n🎉 All scenarios completed!")
    print("👀 Check the Temporal Web UI to see retry attempts and failures")

if __name__ == "__main__":
    asyncio.run(main())