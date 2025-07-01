# 🚦 Lab 3: Retry and Timeout Handling

**Goal:** Handle transient failures gracefully.

- Set retry policy in `ActivityOptions`
- Add intentional failure in activity
- Add start-to-close timeout
- Show retry attempts in Web UI

# Lab 3: Retry and Timeout Handling

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- **Understand failure handling**: Learn why retry and timeout mechanisms are critical in distributed systems
- **Configure retry policies**: Set up automatic retry strategies for failed activities
- **Implement timeouts**: Add time limits to prevent activities from running indefinitely
- **Simulate failures**: Create controlled failure scenarios to test reliability mechanisms
- **Monitor retry behavior**: Observe retry attempts and failure patterns in Temporal Web UI
- **Optimize resilience**: Design fault-tolerant workflows that handle transient failures gracefully

## 📚 Background

### Why Retry and Timeout Handling Matters

In distributed systems, failures are inevitable. Network issues, service outages, and temporary resource constraints can cause activities to fail. Temporal's built-in retry and timeout mechanisms help build resilient applications that can recover from these transient failures automatically.

### Types of Failures in Distributed Systems

| Failure Type | Description | Examples | Temporal Solution |
|--------------|-------------|----------|------------------|
| **Transient** | Temporary issues that resolve themselves | Network hiccups, rate limiting | Automatic retries |
| **Intermittent** | Sporadic failures with periods of success | Overloaded services, timeouts | Retry with backoff |
| **Persistent** | Long-lasting issues requiring intervention | Invalid credentials, missing resources | Retry limits + alerts |
| **Timeout** | Operations taking too long to complete | Slow API calls, database queries | Time-based limits |

### Temporal's Reliability Features

#### Retry Policies
- **Automatic Retries**: Failed activities are automatically retried based on policy
- **Exponential Backoff**: Increasing delays between retry attempts
- **Maximum Attempts**: Limits to prevent infinite retry loops
- **Retry Conditions**: Specify which types of errors should trigger retries

#### Timeout Configurations
- **Start-to-Close Timeout**: Maximum time from activity start to completion
- **Schedule-to-Start Timeout**: Maximum time activity can wait in queue
- **Schedule-to-Close Timeout**: Total time including queuing and execution
- **Heartbeat Timeout**: Maximum time between activity heartbeats

### Real-World Benefits
- **Improved Reliability**: Automatic recovery from transient failures
- **Reduced Manual Intervention**: Less need for human intervention in failure scenarios
- **Better User Experience**: Transparent handling of temporary issues
- **Cost Efficiency**: Optimal resource usage through intelligent retry strategies

## 🛠 Prerequisites

### Poridhi Lab Environment:
- Completion of **Lab 2** (Hello World Workflow)
- Access to Poridhi Lab with VS Code interface
- **Docker & Docker Compose**: ✅ Pre-installed in Poridhi Lab
- **Web Browser**: For accessing Temporal Web UI through load balancer
- **Understanding**: Basic knowledge of workflows and activities from previous labs

### Verify Prerequisites
```bash
# Open VS Code terminal and verify setup
cd lab-3
docker --version
docker-compose --version
```

## 📁 Project Structure

You'll create the following structure in your lab-3 directory:

```
lab-3/
├── docker-compose.yml                    # Temporal server configuration
├── retryAndTimeoutHandlingWorkflow/     # Enhanced workflow implementation
│   ├── Dockerfile                       # Worker container setup
│   ├── compose_greeting_activity.py    # Activity with failure simulation
│   ├── greeting_workflow.py            # Workflow with retry policies
│   ├── worker.py                       # Worker service
│   ├── start_workflow.py               # Workflow starter
│   └── requirements.txt                # Python dependencies
└── README.md                           # This documentation
```

## 🚀 Lab Implementation

### Step 1: Set Up Project Structure

Open VS Code terminal in Poridhi Lab and set up the lab-3 environment:

```bash
# Navigate to lab-3 directory
cd lab-3

# Create workflow directory
mkdir retryAndTimeoutHandlingWorkflow

# Verify structure
ls -la
```

### Step 2: Create Docker Compose Configuration

Create `docker-compose.yml` in the lab-3 directory:

```yaml
version: '3.8'

services:
  temporal:
    image: temporalio/admin-tools:latest
    ports:
      - "7233:7233"  # Temporal Server API
      - "8233:8233"  # Web UI Dashboard
    entrypoint: []
    command: ["temporal", "server", "start-dev", "--ui-port", "8233", "--ip", "0.0.0.0"]

  worker:
    build: ./retryAndTimeoutHandlingWorkflow
    volumes:
      - ./retryAndTimeoutHandlingWorkflow:/app
    depends_on:
      - temporal
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    command: ["python", "worker.py"]
```

### Step 3: Create Enhanced Container Setup

Create `retryAndTimeoutHandlingWorkflow/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy workflow code
COPY . .

# Keep container running for development
CMD ["tail", "-f", "/dev/null"]
```

Create `retryAndTimeoutHandlingWorkflow/requirements.txt`:

```
temporalio==1.5.0
```

### Step 4: Implement Enhanced Activity with Failure Simulation

Create `retryAndTimeoutHandlingWorkflow/compose_greeting_activity.py`:

```python
import random
import time
from temporalio import activity
from typing import Optional

@activity.defn
async def unreliable_greeting_activity(name: str, failure_rate: float = 0.7) -> str:
    """
    An activity that simulates real-world failures.
    
    Args:
        name: The name to greet
        failure_rate: Probability of failure (0.0 to 1.0)
    
    Returns:
        A greeting message if successful
        
    Raises:
        Exception: Simulated transient failure
    """
    
    # Get activity info for logging
    info = activity.info()
    attempt = info.attempt
    
    print(f"🔄 Activity attempt #{attempt} for name: {name}")
    
    # Simulate network delay
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    # Simulate failures based on failure rate
    if random.random() < failure_rate:
        error_types = [
            "NetworkTimeoutError: Connection timed out",
            "ServiceUnavailableError: External service temporarily unavailable", 
            "RateLimitError: Rate limit exceeded, please retry later",
            "DatabaseConnectionError: Temporary database connection issue"
        ]
        error_message = random.choice(error_types)
        print(f"❌ Activity failed on attempt #{attempt}: {error_message}")
        raise Exception(f"Simulated failure: {error_message}")
    
    # Success case
    success_message = f"Hello, {name}! (Successful on attempt #{attempt})"
    print(f"✅ Activity succeeded on attempt #{attempt}")
    return success_message

@activity.defn 
async def slow_processing_activity(data: str, processing_time: int = 10) -> str:
    """
    An activity that takes a long time to complete (for timeout testing).
    
    Args:
        data: Data to process
        processing_time: Time in seconds to simulate processing
        
    Returns:
        Processed data result
    """
    
    info = activity.info()
    print(f"🐌 Starting slow processing activity (attempt #{info.attempt})")
    print(f"⏱️  Will take {processing_time} seconds to complete")
    
    # Simulate long-running processing
    for i in range(processing_time):
        await asyncio.sleep(1)
        print(f"⏳ Processing... {i+1}/{processing_time} seconds elapsed")
        
        # Send heartbeat to indicate activity is still alive
        activity.heartbeat(f"Processing step {i+1}/{processing_time}")
    
    result = f"Processed: {data} (completed after {processing_time}s)"
    print(f"✅ Slow processing completed: {result}")
    return result

# Add this import at the top
import asyncio
```

### Step 5: Create Workflow with Retry Policies and Timeouts

Create `retryAndTimeoutHandlingWorkflow/greeting_workflow.py`:

```python
from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Optional

# Import activities
with workflow.unsafe.imports_passed_through():
    from compose_greeting_activity import unreliable_greeting_activity, slow_processing_activity

@workflow.defn
class RetryAndTimeoutWorkflow:
    """
    Workflow demonstrating retry policies and timeout handling.
    
    This workflow showcases:
    - Automatic retry on transient failures
    - Exponential backoff strategies  
    - Maximum retry limits
    - Various timeout configurations
    """
    
    @workflow.run
    async def run(self, name: str, scenario: str = "retry_demo") -> str:
        """
        Run different failure handling scenarios.
        
        Args:
            name: Name for greeting
            scenario: Type of demo ("retry_demo", "timeout_demo", "heartbeat_demo")
        """
        
        if scenario == "retry_demo":
            return await self._retry_demonstration(name)
        elif scenario == "timeout_demo":
            return await self._timeout_demonstration(name)
        elif scenario == "heartbeat_demo":
            return await self._heartbeat_demonstration(name)
        else:
            return await self._comprehensive_demo(name)
    
    async def _retry_demonstration(self, name: str) -> str:
        """Demonstrate retry policies with an unreliable activity."""
        
        # Configure aggressive retry policy for demonstration
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),      # Start with 1s delay
            backoff_coefficient=2.0,                    # Double delay each time
            maximum_interval=timedelta(seconds=10),     # Max 10s between retries
            maximum_attempts=5,                         # Try up to 5 times
            non_retryable_error_types=["PermanentError"] # Don't retry these errors
        )
        
        try:
            result = await workflow.execute_activity(
                unreliable_greeting_activity,
                args=[name, 0.7],  # 70% failure rate
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy
            )
            return f"🎉 Retry Demo Success: {result}"
            
        except Exception as e:
            return f"❌ Retry Demo Failed after all attempts: {str(e)}"
    
    async def _timeout_demonstration(self, name: str) -> str:
        """Demonstrate timeout handling with a slow activity."""
        
        # Configure short timeout to trigger timeout behavior
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_attempts=3
        )
        
        try:
            result = await workflow.execute_activity(
                slow_processing_activity,
                args=[f"data_for_{name}", 15],  # 15 second processing time
                start_to_close_timeout=timedelta(seconds=8),  # But only 8s timeout
                retry_policy=retry_policy
            )
            return f"🎉 Timeout Demo Success: {result}"
            
        except Exception as e:
            return f"⏰ Timeout Demo Failed: {str(e)}"
    
    async def _heartbeat_demonstration(self, name: str) -> str:
        """Demonstrate heartbeat mechanism with long-running activity."""
        
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_attempts=2
        )
        
        try:
            result = await workflow.execute_activity(
                slow_processing_activity,
                args=[f"heartbeat_data_{name}", 8],  # 8 second processing
                start_to_close_timeout=timedelta(seconds=20),  # Generous timeout
                heartbeat_timeout=timedelta(seconds=3),        # Heartbeat every 3s
                retry_policy=retry_policy
            )
            return f"💓 Heartbeat Demo Success: {result}"
            
        except Exception as e:
            return f"💔 Heartbeat Demo Failed: {str(e)}"
    
    async def _comprehensive_demo(self, name: str) -> str:
        """Run multiple activities with different failure scenarios."""
        
        results = []
        
        # Activity 1: Quick retry demo
        quick_retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_attempts=3
        )
        
        try:
            result1 = await workflow.execute_activity(
                unreliable_greeting_activity,
                args=[f"{name}_quick", 0.5],  # 50% failure rate
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=quick_retry_policy
            )
            results.append(f"Quick Retry: {result1}")
        except Exception as e:
            results.append(f"Quick Retry Failed: {str(e)}")
        
        # Activity 2: Conservative processing
        conservative_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            backoff_coefficient=1.5,
            maximum_attempts=2
        )
        
        try:
            result2 = await workflow.execute_activity(
                slow_processing_activity,
                args=[f"conservative_{name}", 5],  # 5 second processing
                start_to_close_timeout=timedelta(seconds=15),
                retry_policy=conservative_policy
            )
            results.append(f"Conservative: {result2}")
        except Exception as e:
            results.append(f"Conservative Failed: {str(e)}")
        
        return " | ".join(results)
```

### Step 6: Create Worker and Starter Scripts

Create `retryAndTimeoutHandlingWorkflow/worker.py`:

```python
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
```

Create `retryAndTimeoutHandlingWorkflow/start_workflow.py`:

```python
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
```

### Step 7: Deploy and Configure Load Balancer

```bash
# Build and start services
docker-compose up --build -d

# Verify containers are running
docker-compose ps

# Check worker logs
docker-compose logs -f worker
```

#### Configure Load Balancer
1. Get your lab instance IP: `ifconfig eth0`
2. **Create Load Balancer** in Poridhi Lab interface:
   - **Enter IP**: Your lab instance eth0 IP address
   - **Enter Port**: `8233`
3. **Click Create**

### Step 8: Execute Retry and Timeout Demonstrations

#### Run All Scenarios
```bash
# Execute all failure handling scenarios
docker-compose exec worker python start_workflow.py
```

#### Run Individual Scenarios
```bash
# Retry demonstration only
docker-compose exec temporal temporal workflow start \
  --task-queue retry-timeout-task-queue \
  --type RetryAndTimeoutWorkflow \
  --input '["TestUser", "retry_demo"]' \
  --workflow-id retry-demo-manual

# Timeout demonstration only
docker-compose exec temporal temporal workflow start \
  --task-queue retry-timeout-task-queue \
  --type RetryAndTimeoutWorkflow \
  --input '["TestUser", "timeout_demo"]' \
  --workflow-id timeout-demo-manual
```

### Step 9: Observe Retry Behavior in Web UI

#### Access the Web UI
1. **Open Temporal Web UI**: Use your load balancer URL
2. **Navigate to Workflows**: Click "Workflows" in sidebar
3. **Select Namespace**: Choose "default"

#### What to Look For

| Workflow State | What It Means | UI Indicators |
|---------------|---------------|---------------|
| **Running** | Workflow in progress, possibly retrying | Yellow/orange status |
| **Completed** | All retries successful | Green checkmark |
| **Failed** | All retry attempts exhausted | Red X mark |
| **Timed Out** | Activity exceeded timeout limits | Clock icon |

#### Detailed Investigation
1. **Click on any workflow** to see detailed execution
2. **Examine Activity History**:
   - Multiple activity attempts (retries)
   - Timestamps showing retry intervals
   - Error messages for failed attempts
3. **Review Timeline**:
   - Activity scheduling events
   - Retry intervals and backoff progression
   - Final success or failure

## 🔍 Understanding Retry and Timeout Behavior

### Retry Policy Analysis

#### What You Should Observe
- **Multiple Activity Attempts**: Failed activities appear multiple times in the workflow history
- **Exponential Backoff**: Increasing delays between retry attempts
- **Eventual Success**: Most activities succeed after 1-3 retries (due to simulated failures)
- **Retry Exhaustion**: Some workflows fail after all retry attempts

#### Retry Timeline Example
```
Attempt 1: Failed immediately (0s)
Attempt 2: Failed after 1s delay  
Attempt 3: Failed after 2s delay
Attempt 4: Failed after 4s delay
Attempt 5: Success after 8s delay
```

### Timeout Behavior Analysis

#### Timeout Types Demonstrated
- **Start-to-Close**: Activity must complete within specified time
- **Heartbeat**: Activity must send heartbeats regularly during execution
- **Schedule-to-Start**: Activity must start within specified time (not explicitly shown)

#### Timeout Patterns
- Activities exceeding `start_to_close_timeout` are terminated
- Activities failing to heartbeat are considered failed
- Timed-out activities can be retried based on retry policy

## 🧪 Experimentation

### Try These Variations

#### 1. Adjust Failure Rates
```python
# In compose_greeting_activity.py, modify failure rates
await unreliable_greeting_activity(name, 0.9)  # 90% failure rate
await unreliable_greeting_activity(name, 0.1)  # 10% failure rate
```

#### 2. Experiment with Retry Policies
```python
# Conservative retry policy
retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=5),
    backoff_coefficient=1.0,  # No exponential backoff
    maximum_attempts=2        # Only 2 attempts
)

# Aggressive retry policy  
retry_policy = RetryPolicy(
    initial_interval=timedelta(milliseconds=100),
    backoff_coefficient=3.0,  # Triple delay each time
    maximum_attempts=10       # Many attempts
)
```

#### 3. Test Different Timeouts
```python
# Very short timeout (will likely fail)
start_to_close_timeout=timedelta(seconds=2)

# Very long timeout (will likely succeed)
start_to_close_timeout=timedelta(seconds=60)
```

#### 4. Create Custom Failure Scenarios
```python
# Add to compose_greeting_activity.py
@activity.defn
async def database_activity(query: str) -> str:
    """Simulate database connectivity issues."""
    if random.random() < 0.3:
        raise Exception("Database connection timeout")
    if random.random() < 0.2:
        raise Exception("Database deadlock detected")
    return f"Query result for: {query}"
```

## 🔧 Troubleshooting

### Common Issues

#### Activities Not Retrying
```bash
# Check if retry policy is configured
docker-compose logs worker | grep -i retry

# Verify activity registration
docker-compose exec worker python -c "from compose_greeting_activity import *; print('Activities loaded')"
```

#### Timeouts Not Working
```bash
# Check system time and timezone
docker-compose exec worker date

# Verify timeout configuration in logs
docker-compose logs worker | grep -i timeout
```

#### Web UI Not Showing Retries
```bash
# Refresh the Web UI page
# Check workflow is still running (retries take time)
docker-compose exec temporal temporal workflow list --namespace default
```

## 🧹 Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes and clean up
docker-compose down -v
docker system prune -a
```

**Remove Load Balancer**: Delete the load balancer configuration in Poridhi Lab interface.

## 🎓 Key Takeaways

- **Retry Policies** enable automatic recovery from transient failures without manual intervention
- **Exponential Backoff** prevents overwhelming failed services while providing quick recovery
- **Timeouts** prevent activities from running indefinitely and consuming resources
- **Heartbeats** allow long-running activities to signal they're still alive and making progress
- **Web UI** provides detailed visibility into retry attempts and failure patterns
- **Failure Simulation** helps test and validate resilience mechanisms in controlled environments
- **Policy Configuration** allows fine-tuning retry behavior for different types of activities

## 🚀 Next Steps

- **Lab 4**: Implement long-running workflows with signals and queries
- **Lab 5**: Explore parent-child workflow relationships
- **Advanced**: Create custom retry policies based on error types
- **Production**: Implement monitoring and alerting for workflow failures

## 📚 Additional Resources

- [Temporal Retry Policies](https://docs.temporal.io/concepts/what-is-a-retry-policy)
- [Activity Timeouts](https://docs.temporal.io/concepts/what-is-an-activity-timeout)
- [Error Handling Best Practices](https://docs.temporal.io/application-development/foundations#activity-heartbeats)
- [Observability and Monitoring](https://docs.temporal.io/concepts/what-is-observability)