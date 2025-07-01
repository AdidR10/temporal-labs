# 📦 Lab 4: Signals and Queries

**Goal:** Interact with running workflows.

- Create a long-running counter workflow
- Send signals to increment count
- Query current count at any time
- Practice sending signal/query via CLI


# Long Running Counter Workflow

A Temporal workflow example that demonstrates a long-running counter with signal and query capabilities.

## Quick Start

1. **Navigate to the workflow directory:**
   ```bash
   cd longRunningCounterWorkflow
   ```

2. **Start the services:**
   ```bash
   docker-compose up --build
   ```

3. **Run the workflow:**
   ```bash
   docker-compose exec worker python start_workflow.py
   ```

4. **Access Temporal Web UI:**
   Open [http://localhost:8233](http://localhost:8233) and note the workflow ID.

## Workflow Operations

### Send Signal (Increment Counter)
```bash
docker-compose exec temporal tctl --namespace default workflow signal \
  --workflow_id <workflow-id> --name increment
```

### Query Counter Value
```bash
docker-compose exec temporal temporal workflow query \
  --workflow-id <workflow-id> --type get_count
```

## Notes
- The workflow runs indefinitely and prints the counter every 10 seconds
- Use signals to increment the counter
- Use queries to check the current count value


# Lab 4: Signals and Queries

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- **Understand workflow communication**: Learn how to interact with running workflows in real-time
- **Implement signals**: Send data and commands to workflows while they're executing
- **Use queries**: Retrieve current state and data from running workflows
- **Create long-running workflows**: Build workflows that run indefinitely and maintain state
- **Master CLI interactions**: Use Temporal CLI to send signals and execute queries
- **Design interactive systems**: Build workflows that respond to external events and user interactions

## 📚 Background

### Why Signals and Queries Matter

Traditional batch workflows run to completion without external interaction. However, many real-world scenarios require **dynamic interaction** with running workflows - updating parameters, checking status, or triggering actions based on external events.

### Temporal's Interactive Features

#### Signals
**Signals** allow you to send data to a running workflow, enabling dynamic updates and external control.

| Signal Characteristic | Description | Use Cases |
|----------------------|-------------|-----------|
| **Asynchronous** | Fire-and-forget, doesn't wait for response | User actions, external events |
| **Durable** | Persisted and replayed during recovery | Critical state updates |
| **Ordered** | Processed in the order they're received | Sequential operations |
| **Type-Safe** | Strongly typed parameters | Data integrity |

#### Queries
**Queries** allow you to retrieve current state from a running workflow without affecting its execution.

| Query Characteristic | Description | Use Cases |
|---------------------|-------------|-----------|
| **Synchronous** | Returns immediate response | Status checks, dashboards |
| **Read-Only** | Cannot modify workflow state | Safe data access |
| **Consistent** | Returns current workflow state | Real-time monitoring |
| **Fast** | Low latency operations | User interfaces |

### Real-World Applications

#### E-commerce Order Processing
- **Signals**: Cancel order, update shipping address, apply discount
- **Queries**: Check order status, get tracking info, view current total

#### IoT Device Management
- **Signals**: Change configuration, trigger maintenance, update firmware
- **Queries**: Get sensor readings, check device status, view metrics

#### Financial Trading Systems
- **Signals**: Modify trading parameters, stop trading, update limits
- **Queries**: Get current positions, check P&L, view trade history

#### Game Servers
- **Signals**: Player actions, game events, admin commands
- **Queries**: Player stats, game state, leaderboards

### Communication Patterns

```
┌─────────────┐    Signals     ┌─────────────────┐
│   External  │──────────────► │   Running       │
│   Systems   │                │   Workflow      │
│             │◄─────────────  │                 │
└─────────────┘    Queries     └─────────────────┘
```

## 🛠 Prerequisites

### Poridhi Lab Environment:
- Completion of **Lab 3** (Retry and Timeout Handling)
- Access to Poridhi Lab with VS Code interface
- **Docker & Docker Compose**: ✅ Pre-installed in Poridhi Lab
- **Web Browser**: For accessing Temporal Web UI through load balancer
- **Understanding**: Knowledge of workflows, activities, and fault tolerance

### Verify Prerequisites
```bash
# Open VS Code terminal and verify setup
cd lab-4
docker --version
docker-compose --version
```

## 📁 Project Structure

You'll create the following structure in your lab-4 directory:

```
lab-4/
├── docker-compose.yml                # Temporal server configuration
├── longRunningCounterWorkflow/       # Interactive workflow implementation
│   ├── Dockerfile                    # Worker container setup
│   ├── counter_workflow.py          # Long-running workflow with signals/queries
│   ├── worker.py                    # Worker service
│   ├── start_workflow.py            # Workflow starter
│   └── requirements.py             # Python dependencies
└── README.md                        # This documentation
```

## 🚀 Lab Implementation

### Step 1: Set Up Project Structure

Open VS Code terminal in Poridhi Lab and navigate to your lab-4 directory:

```bash
# Navigate to lab-4 directory
cd lab-4

# Verify the longRunningCounterWorkflow directory exists
ls -la longRunningCounterWorkflow/
```

### Step 2: Understand the Docker Configuration

The `docker-compose.yml` should already be configured:

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
    build: ./longRunningCounterWorkflow
    volumes:
      - ./longRunningCounterWorkflow:/app
    depends_on:
      - temporal
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    command: ["python", "worker.py"]
```

### Step 3: Examine the Counter Workflow

Let's look at the existing `longRunningCounterWorkflow/counter_workflow.py` to understand signals and queries:

<function_calls>
<invoke name="read_file">
<parameter name="target_file">lab-4/longRunningCounterWorkflow/counter_workflow.py
```
</file>

<edit_instructions>
<message_from_colleague>
I'm completely rewriting the lab-4 README to create comprehensive educational documentation focused on signals and queries, following the same structure as the previous labs.

```lab-4/README.md
<code_block_to_apply_changes_from>
```
</message_from_colleague>

<rewritten_file>
```
# Lab 4: Signals and Queries

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- **Understand workflow communication**: Learn how to interact with running workflows in real-time
- **Implement signals**: Send data and commands to workflows while they're executing
- **Use queries**: Retrieve current state and data from running workflows
- **Create long-running workflows**: Build workflows that run indefinitely and maintain state
- **Master CLI interactions**: Use Temporal CLI to send signals and execute queries
- **Design interactive systems**: Build workflows that respond to external events and user interactions

## 📚 Background

### Why Signals and Queries Matter

Traditional batch workflows run to completion without external interaction. However, many real-world scenarios require **dynamic interaction** with running workflows - updating parameters, checking status, or triggering actions based on external events.

### Temporal's Interactive Features

#### Signals
**Signals** allow you to send data to a running workflow, enabling dynamic updates and external control.

| Signal Characteristic | Description | Use Cases |
|----------------------|-------------|-----------|
| **Asynchronous** | Fire-and-forget, doesn't wait for response | User actions, external events |
| **Durable** | Persisted and replayed during recovery | Critical state updates |
| **Ordered** | Processed in the order they're received | Sequential operations |
| **Type-Safe** | Strongly typed parameters | Data integrity |

#### Queries
**Queries** allow you to retrieve current state from a running workflow without affecting its execution.

| Query Characteristic | Description | Use Cases |
|---------------------|-------------|-----------|
| **Synchronous** | Returns immediate response | Status checks, dashboards |
| **Read-Only** | Cannot modify workflow state | Safe data access |
| **Consistent** | Returns current workflow state | Real-time monitoring |
| **Fast** | Low latency operations | User interfaces |

### Real-World Applications

#### E-commerce Order Processing
- **Signals**: Cancel order, update shipping address, apply discount
- **Queries**: Check order status, get tracking info, view current total

#### IoT Device Management
- **Signals**: Change configuration, trigger maintenance, update firmware
- **Queries**: Get sensor readings, check device status, view metrics

#### Financial Trading Systems
- **Signals**: Modify trading parameters, stop trading, update limits
- **Queries**: Get current positions, check P&L, view trade history

#### Game Servers
- **Signals**: Player actions, game events, admin commands
- **Queries**: Player stats, game state, leaderboards

### Communication Patterns

```
┌─────────────┐    Signals     ┌─────────────────┐
│   External  │──────────────► │   Running       │
│   Systems   │                │   Workflow      │
│             │◄─────────────  │                 │
└─────────────┘    Queries     └─────────────────┘
```

## 🛠 Prerequisites

### Poridhi Lab Environment:
- Completion of **Lab 3** (Retry and Timeout Handling)
- Access to Poridhi Lab with VS Code interface
- **Docker & Docker Compose**: ✅ Pre-installed in Poridhi Lab
- **Web Browser**: For accessing Temporal Web UI through load balancer
- **Understanding**: Knowledge of workflows, activities, and fault tolerance

### Verify Prerequisites
```bash
# Open VS Code terminal and verify setup
cd lab-4
docker --version
docker-compose --version
```

## 📁 Project Structure

You'll work with the following structure in your lab-4 directory:

```
lab-4/
├── docker-compose.yml                # Temporal server configuration
├── longRunningCounterWorkflow/       # Interactive workflow implementation
│   ├── Dockerfile                    # Worker container setup
│   ├── counter_workflow.py          # Long-running workflow with signals/queries
│   ├── worker.py                    # Worker service
│   ├── start_workflow.py            # Workflow starter
│   └── requirements.py             # Python dependencies
└── README.md                        # This documentation
```

## 🚀 Lab Implementation

### Step 1: Set Up Project Structure

Open VS Code terminal in Poridhi Lab and navigate to your lab-4 directory:

```bash
# Navigate to lab-4 directory
cd lab-4

# Verify the longRunningCounterWorkflow directory exists
ls -la longRunningCounterWorkflow/
```

### Step 2: Understand the Docker Configuration

The `docker-compose.yml` should already be configured:

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
    build: ./longRunningCounterWorkflow
    volumes:
      - ./longRunningCounterWorkflow:/app
    depends_on:
      - temporal
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    command: ["python", "worker.py"]
```

### Step 3: Examine the Counter Workflow

The existing `longRunningCounterWorkflow/counter_workflow.py` demonstrates signals and queries:

```python
from temporalio import workflow
from datetime import timedelta

@workflow.defn(name="CounterWorkflow")
class CounterWorkflow:
    def __init__(self):
        self.count = 0

    @workflow.run
    async def run(self) -> int:
        """
        Long-running workflow that maintains state and responds to signals.
        This workflow runs indefinitely, demonstrating persistent state management.
        """
        while True:
            # Sleep for 10 seconds between status updates
            await workflow.sleep(timedelta(seconds=10))
            
            # Print current status (only when not replaying)
            if not workflow.unsafe.is_replaying():
                print(f"Current count: {self.count}")

    @workflow.signal
    async def increment(self) -> None:
        """
        Signal handler to increment the counter.
        Signals allow external systems to send data to running workflows.
        """
        self.count += 1
        if not workflow.unsafe.is_replaying():
            print(f"🔔 Signal received! Count incremented to: {self.count}")

    @workflow.query
    def get_count(self) -> int:
        """
        Query handler to retrieve current counter value.
        Queries allow external systems to read workflow state without modification.
        """
        return self.count
```

#### Key Concepts Demonstrated

| Component | Purpose | Code Pattern |
|-----------|---------|--------------|
| **Long-running Loop** | Keeps workflow alive indefinitely | `while True:` with `workflow.sleep()` |
| **Signal Handler** | Receives external commands | `@workflow.signal` decorator |
| **Query Handler** | Provides state access | `@workflow.query` decorator |
| **State Management** | Maintains workflow state | Instance variable `self.count` |
| **Replay Safety** | Prevents duplicate logging | `workflow.unsafe.is_replaying()` check |

### Step 4: Examine the Worker Service

The `longRunningCounterWorkflow/worker.py` registers the workflow:

```python
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
```

### Step 5: Deploy and Configure Load Balancer

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

### Step 6: Start the Counter Workflow

```bash
# Start the counter workflow
docker-compose exec worker python start_workflow.py
```

The workflow will start and you should see output like:
```
🚀 Starting CounterWorkflow...
📋 Workflow ID: counter-workflow-1703845200
✅ Workflow started successfully!
Current count: 0
Current count: 0
...
```

**Important**: Note the **Workflow ID** from the output - you'll need it for sending signals and queries!

### Step 7: Access Web UI and Monitor Workflow

1. **Open Temporal Web UI**: Use your load balancer URL
2. **Navigate to Workflows**: Click "Workflows" in sidebar
3. **Find Your Workflow**: Look for the CounterWorkflow
4. **Observe the Running State**: The workflow should show as "Running"

#### What to Look For in Web UI
- **Status**: Running (green)
- **Run ID**: Unique execution identifier
- **Task Queue**: `long-running-counter-task-queue`
- **History**: Shows workflow started event

### Step 8: Send Signals to the Workflow

#### Using Temporal CLI
```bash
# Replace <workflow-id> with your actual workflow ID
export WORKFLOW_ID="counter-workflow-1703845200"

# Send increment signal
docker-compose exec temporal temporal workflow signal \
  --workflow-id $WORKFLOW_ID \
  --name increment \
  --namespace default

# Send multiple signals
docker-compose exec temporal temporal workflow signal \
  --workflow-id $WORKFLOW_ID \
  --name increment \
  --namespace default

docker-compose exec temporal temporal workflow signal \
  --workflow-id $WORKFLOW_ID \
  --name increment \
  --namespace default
```

#### Observe Signal Effects
After sending signals, check the worker logs:
```bash
docker-compose logs -f worker
```

You should see:
```
🔔 Signal received! Count incremented to: 1
🔔 Signal received! Count incremented to: 2
🔔 Signal received! Count incremented to: 3
Current count: 3
```

### Step 9: Query Workflow State

#### Get Current Counter Value
```bash
# Query the current count
docker-compose exec temporal temporal workflow query \
  --workflow-id $WORKFLOW_ID \
  --type get_count \
  --namespace default
```

Expected output:
```
Query result: 3
```

#### Multiple Queries
```bash
# Send more signals
docker-compose exec temporal temporal workflow signal \
  --workflow-id $WORKFLOW_ID \
  --name increment \
  --namespace default

# Query again to see updated count
docker-compose exec temporal temporal workflow query \
  --workflow-id $WORKFLOW_ID \
  --type get_count \
  --namespace default
```

### Step 10: Observe in Web UI

#### Signal and Query Events
1. **Refresh the Web UI**
2. **Click on your workflow**
3. **Examine the Timeline**: You should see:
   - **WorkflowTaskScheduled** events
   - **WorkflowTaskCompleted** events
   - **Signal** events for each increment
   - **Query** events for each state request

#### Workflow Details
- **Input and Results**: Shows workflow parameters
- **Timeline**: Complete history of events
- **Query Results**: Shows latest query responses
- **Signals Sent**: List of all signals received

## 🔍 Understanding Signals and Queries

### Signal Behavior Analysis

#### What You Should Observe
- **Immediate Processing**: Signals are processed as soon as the workflow task runs
- **Durable State**: Counter value persists even if containers restart
- **Ordered Processing**: Signals are processed in the order they're sent
- **Event History**: All signals appear in the workflow timeline

#### Signal Flow
```
CLI Command → Temporal Server → Workflow Task → Signal Handler → State Update
```

### Query Behavior Analysis

#### Query Characteristics
- **Immediate Response**: Queries return current state without delay
- **No State Change**: Queries don't modify workflow state
- **Consistent Reads**: Always returns current workflow state
- **No History Impact**: Queries don't appear in workflow execution history

#### Query vs Signal Comparison

| Aspect | Signals | Queries |
|--------|---------|---------|
| **Purpose** | Modify state | Read state |
| **Response** | Asynchronous (fire-and-forget) | Synchronous (immediate response) |
| **Durability** | Persisted in history | Not persisted |
| **Side Effects** | Can change workflow state | Read-only |
| **Performance** | Queued with workflow tasks | Immediate execution |

## 🧪 Experimentation

### Try These Variations

#### 1. Send Rapid Signals
```bash
# Send many signals quickly
for i in {1..10}; do
  docker-compose exec temporal temporal workflow signal \
    --workflow-id $WORKFLOW_ID \
    --name increment \
    --namespace default
  echo "Sent signal #$i"
done

# Query the result
docker-compose exec temporal temporal workflow query \
  --workflow-id $WORKFLOW_ID \
  --type get_count \
  --namespace default
```

#### 2. Create Additional Signal Handlers
Add to `counter_workflow.py`:
```python
@workflow.signal
async def decrement(self) -> None:
    """Signal to decrement the counter."""
    self.count = max(0, self.count - 1)  # Don't go below 0
    if not workflow.unsafe.is_replaying():
        print(f"🔔 Count decremented to: {self.count}")

@workflow.signal  
async def reset(self) -> None:
    """Signal to reset the counter."""
    self.count = 0
    if not workflow.unsafe.is_replaying():
        print(f"🔔 Counter reset to: {self.count}")
```

#### 3. Add More Query Types
```python
@workflow.query
def get_status(self) -> str:
    """Query to get workflow status information."""
    return f"Counter at {self.count}, workflow running for {self.get_runtime()}"

@workflow.query
def is_even(self) -> bool:
    """Query to check if counter is even."""
    return self.count % 2 == 0
```

#### 4. Test Signal Parameters
```python
@workflow.signal
async def add_value(self, value: int) -> None:
    """Signal to add a specific value to the counter."""
    self.count += value
    if not workflow.unsafe.is_replaying():
        print(f"🔔 Added {value}, count now: {self.count}")
```

Send with parameters:
```bash
# Send signal with parameter (requires JSON input)
docker-compose exec temporal temporal workflow signal \
  --workflow-id $WORKFLOW_ID \
  --name add_value \
  --input '5' \
  --namespace default
```

## 🔧 Troubleshooting

### Common Issues

#### Workflow Not Receiving Signals
```bash
# Check if workflow is running
docker-compose exec temporal temporal workflow describe \
  --workflow-id $WORKFLOW_ID \
  --namespace default

# Verify signal name spelling
docker-compose exec temporal temporal workflow signal \
  --workflow-id $WORKFLOW_ID \
  --name increment \
  --namespace default
```

#### Query Not Returning Data
```bash
# Check query type name
docker-compose exec temporal temporal workflow query \
  --workflow-id $WORKFLOW_ID \
  --type get_count \
  --namespace default

# List available queries
docker-compose exec temporal temporal workflow describe \
  --workflow-id $WORKFLOW_ID \
  --namespace default
```

#### Worker Not Processing
```bash
# Check worker logs
docker-compose logs worker

# Restart worker if needed
docker-compose restart worker
```

## 🧹 Cleanup

### Stop the Long-Running Workflow
```bash
# Terminate the workflow
docker-compose exec temporal temporal workflow terminate \
  --workflow-id $WORKFLOW_ID \
  --reason "Lab completed" \
  --namespace default

# Stop all services
docker-compose down

# Clean up resources
docker-compose down -v
docker system prune -a
```

**Remove Load Balancer**: Delete the load balancer configuration in Poridhi Lab interface.

## 🎓 Key Takeaways

- **Signals** enable real-time communication with running workflows without interrupting execution
- **Queries** provide immediate access to workflow state for monitoring and dashboards
- **Long-running workflows** can maintain state indefinitely and respond to external events
- **Temporal CLI** provides powerful tools for interacting with workflows in development and production
- **Durable state** ensures workflow data persists across restarts and failures
- **Event sourcing** means all signals and state changes are recorded in workflow history
- **Interactive patterns** enable building responsive, event-driven applications

## 🚀 Next Steps

- **Lab 5**: Explore parent-child workflow relationships and workflow composition
- **Advanced**: Implement workflow cancellation and timeout patterns
- **Production**: Add monitoring and alerting for workflow signals and queries
- **Integration**: Connect workflows to external APIs and user interfaces

## 📚 Additional Resources

- [Temporal Signals Documentation](https://docs.temporal.io/concepts/what-is-a-signal)
- [Temporal Queries Documentation](https://docs.temporal.io/concepts/what-is-a-query)
- [Long-Running Workflow Patterns](https://docs.temporal.io/application-development/foundations#long-running-workflows)
- [CLI Reference Guide](https://docs.temporal.io/cli/workflow)