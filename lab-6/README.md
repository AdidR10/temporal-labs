# 🛰️ Lab 6: Cron Scheduling & External Triggers

## 🎯 Learning Objectives

By the end of this lab, you will understand:
- **Cron Scheduling**: How to schedule workflows to run automatically at specific times
- **HTTP Triggers**: How to start workflows via REST API endpoints
- **Signal Integration**: How external systems can communicate with running workflows
- **Multi-trigger Workflows**: Building workflows that can be started in multiple ways
- **External System Integration**: Creating APIs that bridge external services with Temporal

## 🏗️ Background Concepts

### Cron Scheduling in Temporal
Temporal provides built-in support for scheduled workflows using cron expressions:
- **Schedule Objects**: Define when workflows should run
- **Cron Expressions**: Standard Unix-style scheduling syntax (minute, hour, day, month, weekday)
- **Automatic Retries**: Failed scheduled workflows are automatically retried
- **Schedule Management**: Create, update, pause, and delete schedules programmatically

### External Triggers & HTTP Integration
Real-world applications often need to:
- **Trigger Workflows from Web Apps**: Start workflows based on user actions
- **Integrate with Webhooks**: Respond to external system events
- **Signal Running Workflows**: Send data to workflows from external sources
- **Query Workflow State**: Check workflow progress from external systems

### Signal-Driven Workflows
Signals enable real-time communication:
- **Asynchronous Communication**: External systems send data without blocking
- **Dynamic Behavior**: Workflows can change behavior based on incoming signals
- **Event Aggregation**: Collect multiple signals before processing
- **Graceful Shutdown**: External systems can request workflow termination

## 📁 Lab Structure

```
lab-6/
├── docker-compose.yml          # Multi-service setup with API
├── requirements.txt            # Python dependencies (temporalio, fastapi, uvicorn)
├── Dockerfile                 # Container configuration
└── app/
    ├── cronWorkflow.py        # Signal-enabled workflow with cron support
    ├── main.py               # FastAPI endpoints for external integration
    ├── worker.py             # Workflow worker registration
    ├── activity.py           # Simple activity definition
    └── Dockerfile            # App-specific container config
```

## 🚀 Implementation Guide

### Step 1: Start the Multi-Service Environment

Navigate to the lab-6 directory and start all services:

```bash
cd lab-6
docker-compose up -d
```

This starts three interconnected services:
- **Temporal Server**: Core workflow engine with Web UI (port 8233)
- **Worker Service**: Executes workflows and activities
- **API Service**: FastAPI application for external integration (port 8000)

### Step 2: Configure Load Balancer for External Access

Set up load balancer to access both Temporal Web UI and FastAPI:

```bash
# Get your lab instance IP
ip addr show eth0

# Configure load balancer for Temporal Web UI
# Target: <your-eth0-ip>:8233
# External Port: 8233

# Configure load balancer for FastAPI
# Target: <your-eth0-ip>:8000  
# External Port: 8000
```

### Step 3: Examine the Signal-Enabled Workflow

Let's understand the `CronWorkflow` implementation:

```python
# app/cronWorkflow.py
@workflow.defn
class CronWorkflow:
    def __init__(self):
        self.messages = []      # Collect signals from external systems
        self.should_stop = False
    
    @workflow.signal
    async def add_message(self, message: str):
        """External services can send data via this signal"""
        self.messages.append(message)
    
    @workflow.signal  
    async def stop_processing(self):
        """External services can stop the workflow"""
        self.should_stop = True
    
    @workflow.run
    async def run(self, task_name: str) -> dict:
        # Wait for signals or timeout
        await workflow.wait_condition(
            lambda: self.should_stop or len(self.messages) >= 5,
            timeout=timedelta(seconds=30)
        )   
        
        # Process collected messages
        return {
            "task": task_name,
            "messages_processed": len(self.messages),
            "messages": self.messages,
            "completed_at": str(workflow.now())
        }
```

**Key Features:**
- **Signal Handlers**: `add_message()` and `stop_processing()` receive external data
- **Conditional Waiting**: Workflow waits for either 5 messages or 30-second timeout
- **Event Aggregation**: Collects multiple signals before processing
- **Multi-trigger Support**: Can be started via cron, HTTP, or manual triggers

### Step 4: Explore the FastAPI Integration

The API service provides six endpoints for external integration:

```python
# app/main.py - Key endpoints:

# 1. Manual HTTP trigger
POST /trigger-workflow/{workflow_id}
# Starts workflow immediately via HTTP request

# 2. Cron scheduling  
POST /schedule-workflow/{schedule_id}
# Creates recurring schedule with cron expression

# 3. Schedule deletion
DELETE /schedule-workflow/{schedule_id}
# Deletes/stops a cron schedule

# 4. Signal sending
POST /signal-workflow/{workflow_id}  
# Sends message to running workflow

# 5. Graceful shutdown
POST /stop-workflow/{workflow_id}
# Signals workflow to stop processing

# 6. Result retrieval
GET /workflow-result/{workflow_id}
# Gets final workflow result
```

## 🧪 Hands-On Experimentation

### Experiment 1: Manual HTTP Workflow Triggers

Test direct workflow triggering via HTTP:

```bash
# Trigger a workflow with custom ID
curl -X POST "http://localhost:8000/trigger-workflow/manual-test-001?name=HTTP%20Triggered"

# Check the response - you'll get workflow ID and status
```

Monitor in Temporal Web UI:
1. Access Web UI via your configured load balancer (port 8233)
2. Navigate to "Workflows" section
3. Find workflow ID `manual-test-001`
4. Observe workflow execution and timeline

### Experiment 2: Cron Scheduling Setup

Create automated recurring workflows:

```bash
# Schedule workflow to run every minute
curl -X POST "http://localhost:8000/schedule-workflow/daily-report?cron=*%20*%20*%20*%20*"

# Schedule workflow to run every 5 minutes
curl -X POST "http://localhost:8000/schedule-workflow/frequent-check?cron=*/5%20*%20*%20*%20*"

# Schedule workflow for specific time (e.g., daily at 9 AM)
curl -X POST "http://localhost:8000/schedule-workflow/morning-sync?cron=0%209%20*%20*%20*"
```

**Cron Expression Examples:**
- `* * * * *` - Every minute
- `*/5 * * * *` - Every 5 minutes  
- `0 9 * * *` - Daily at 9:00 AM
- `0 18 * * 1-5` - Weekdays at 6:00 PM
- `0 0 1 * *` - First day of every month

View schedules in Web UI:
1. Navigate to "Schedules" section
2. Observe created schedules and their next run times
3. View triggered workflow executions

**Delete schedules via API:**
```bash
# Delete a specific schedule
curl -X DELETE "http://localhost:8000/schedule-workflow/daily-report"

# Verify schedule is deleted
curl -X DELETE "http://localhost:8000/schedule-workflow/frequent-check"
```

### Experiment 3: Real-Time Signal Communication

Test dynamic signal sending to running workflows:

```bash
# Start a long-running workflow
curl -X POST "http://localhost:8000/trigger-workflow/signal-test-001?name=Signal%20Test"

# Send multiple messages while workflow runs
curl -X POST "http://localhost:8000/signal-workflow/signal-test-001" \
  -H "Content-Type: application/json" \
  -d '{"message": "First external event"}'

curl -X POST "http://localhost:8000/signal-workflow/signal-test-001" \
  -H "Content-Type: application/json" \
  -d '{"message": "Second external event"}'

curl -X POST "http://localhost:8000/signal-workflow/signal-test-001" \
  -H "Content-Type: application/json" \
  -d '{"message": "Third external event"}'

# Check if workflow is still running
curl -X GET "http://localhost:8000/workflow-result/signal-test-001"
```

Monitor signal delivery in Web UI:
1. Find workflow `signal-test-001`
2. Navigate to "History" tab
3. Observe "SignalReceived" events
4. Watch workflow state changes

### Experiment 4: Graceful Workflow Termination

Test controlled workflow shutdown:

```bash
# Start workflow
curl -X POST "http://localhost:8000/trigger-workflow/shutdown-test-001?name=Shutdown%20Test"

# Send stop signal
curl -X POST "http://localhost:8000/stop-workflow/shutdown-test-001"

# Verify workflow completed gracefully
curl -X GET "http://localhost:8000/workflow-result/shutdown-test-001"
```

### Experiment 5: Event Aggregation Patterns

Test workflow message collection behavior:

```bash
# Start workflow for aggregation test
curl -X POST "http://localhost:8000/trigger-workflow/aggregation-test-001?name=Aggregation%20Test"

# Send exactly 5 messages to trigger completion
for i in {1..5}; do
  curl -X POST "http://localhost:8000/signal-workflow/aggregation-test-001" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Event number $i\"}"
  sleep 2
done

# Check final result with all aggregated messages
curl -X GET "http://localhost:8000/workflow-result/aggregation-test-001"
```

### Experiment 6: Complete Schedule Lifecycle Management

Test the full lifecycle of schedule creation, monitoring, and deletion:

```bash
# 1. Create a test schedule (every 2 minutes)
curl -X POST "http://localhost:8000/schedule-workflow/lifecycle-test?cron=*/2%20*%20*%20*%20*"

# 2. Monitor the schedule in Web UI
# Navigate to Schedules section and observe "lifecycle-test" schedule

# 3. Wait for schedule to trigger (2 minutes) and observe workflow executions
# Check Workflows section for executions with "Cron Triggered" name

# 4. Delete the schedule via API
curl -X DELETE "http://localhost:8000/schedule-workflow/lifecycle-test"

# 5. Verify schedule is deleted
docker-compose exec temporal temporal schedule list | grep lifecycle-test || echo "Schedule successfully deleted"
```

**Schedule Lifecycle Monitoring:**
1. **Creation**: Schedule appears in Web UI Schedules section
2. **Execution**: Triggered workflows appear in Workflows section
3. **Deletion**: Schedule disappears from Web UI and stops triggering new workflows
4. **Existing Workflows**: Running workflows continue even after schedule deletion

## 🔍 Advanced Exploration

### Schedule Management via CLI and API

Use Temporal CLI for advanced schedule operations:

```bash
# List all schedules
docker-compose exec temporal temporal schedule list

# Describe specific schedule
docker-compose exec temporal temporal schedule describe --schedule-id daily-report

# Pause schedule
docker-compose exec temporal temporal schedule toggle --schedule-id daily-report --pause

# Resume schedule  
docker-compose exec temporal temporal schedule toggle --schedule-id daily-report --unpause

# Delete schedule via CLI
docker-compose exec temporal temporal schedule delete --schedule-id daily-report
```

**Alternative: Schedule Management via API**

```bash
# Create schedule
curl -X POST "http://localhost:8000/schedule-workflow/api-managed-schedule?cron=0%209%20*%20*%20*"

# Delete schedule via API
curl -X DELETE "http://localhost:8000/schedule-workflow/api-managed-schedule"

# List schedules (CLI only)
docker-compose exec temporal temporal schedule list
```

### Advanced Cron Expressions

Test complex scheduling patterns:

```bash
# Business hours only (9 AM - 5 PM, weekdays)
curl -X POST "http://localhost:8000/schedule-workflow/business-hours?cron=0%209-17%20*%20*%201-5"

# Quarterly reports (first day of quarter at midnight)
curl -X POST "http://localhost:8000/schedule-workflow/quarterly?cron=0%200%201%201,4,7,10%20*"

# High-frequency monitoring (every 30 seconds)
curl -X POST "http://localhost:8000/schedule-workflow/monitoring?cron=*/30%20*%20*%20*%20*"
```

### Multi-Instance Signal Broadcasting

Send signals to multiple workflow instances:

```bash
# Start multiple workflow instances
for i in {1..3}; do
  curl -X POST "http://localhost:8000/trigger-workflow/broadcast-test-00$i?name=Broadcast%20Test%20$i"
done

# Broadcast message to all instances
for i in {1..3}; do
  curl -X POST "http://localhost:8000/signal-workflow/broadcast-test-00$i" \
    -H "Content-Type: application/json" \
    -d '{"message": "Global announcement"}'
done
```

## 🌐 Real-World Integration Patterns

### Webhook Integration Pattern

```python
# Example: Integrate with external webhook
@app.post("/webhook/github")
async def github_webhook(payload: dict):
    """Handle GitHub webhook and trigger deployment workflow"""
    if payload.get("action") == "push":
        workflow_id = f"deploy-{payload['repository']['name']}-{payload['after'][:8]}"
        await client.start_workflow(
            CronWorkflow.run,
            f"Deploy {payload['repository']['name']}",
            id=workflow_id,
            task_queue="lab6-queue",
        )
    return {"status": "processed"}
```

### Event-Driven Architecture

```python
# Example: Message queue integration
@app.post("/process-order")
async def process_order(order_data: dict):
    """Process order and trigger fulfillment workflow"""
    workflow_id = f"order-{order_data['order_id']}"
    
    # Start workflow
    handle = await client.start_workflow(
        CronWorkflow.run,
        f"Process Order {order_data['order_id']}",
        id=workflow_id,
        task_queue="lab6-queue",
    )
    
    # Send order details via signal
    await handle.signal(CronWorkflow.add_message, 
                       f"Order data: {order_data}")
    
    return {"workflow_id": workflow_id, "status": "processing"}
```

## 🎛️ Monitoring & Observability

### API Health Checks

Monitor service health:

```bash
# Check API service status
curl http://localhost:8000/

# Verify Temporal connectivity
curl http://localhost:8000/health
```

### Workflow Metrics Analysis

Use Web UI to analyze workflow patterns:

1. **Schedule Performance**: View schedule execution history and success rates
2. **Signal Latency**: Monitor time between signal sending and processing
3. **Workflow Duration**: Track how long workflows take to complete
4. **Error Patterns**: Identify common failure points in triggered workflows

### Log Analysis

Monitor service logs:

```bash
# View API service logs
docker-compose logs -f api

# View worker logs  
docker-compose logs -f worker

# View Temporal server logs
docker-compose logs -f temporal
```

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

**Issue**: API returns "Connection refused" errors
```bash
# Solution: Verify Temporal server is running
docker-compose ps temporal
docker-compose logs temporal
```

**Issue**: Schedules not triggering workflows
```bash
# Solution: Check schedule configuration
docker-compose exec temporal temporal schedule describe --schedule-id <schedule-id>

# Verify worker is running and registered
docker-compose logs worker

# Check if schedule was accidentally deleted
docker-compose exec temporal temporal schedule list
```

**Issue**: Schedule deletion not working via API
```bash
# Solution: Verify schedule exists before deletion
docker-compose exec temporal temporal schedule list | grep <schedule-id>

# Use CLI deletion as alternative
docker-compose exec temporal temporal schedule delete --schedule-id <schedule-id>
```

**Issue**: Signals not reaching workflows
```bash
# Solution: Verify workflow is running
curl http://localhost:8000/workflow-result/<workflow-id>

# Check signal history in Web UI
# Navigate to workflow → History tab → Look for SignalReceived events
```

**Issue**: FastAPI service not accessible
```bash
# Solution: Check port binding and load balancer
docker-compose ps api
curl http://localhost:8000/
```

**Issue**: Cron expressions not working as expected
```bash
# Solution: Test cron expression syntax
# Use online cron validators or test with frequent expressions first
# Example: Use "*/1 * * * *" (every minute) for testing
```

### Performance Optimization

**High-Frequency Schedules**: For schedules running very frequently (< 1 minute intervals):
- Monitor worker capacity and scale if needed
- Consider batching multiple events in single workflow execution
- Use appropriate timeout values to prevent resource exhaustion

**Large-Scale Signal Handling**: For workflows receiving many signals:
- Implement signal batching in workflow logic
- Set appropriate wait conditions to process signals efficiently
- Monitor memory usage in long-running workflows

## 🎓 Key Takeaways

1. **Multi-Modal Triggering**: Temporal workflows can be started via schedules, HTTP endpoints, CLI, or other workflows
2. **Real-Time Communication**: Signals enable external systems to communicate with running workflows asynchronously
3. **Schedule Flexibility**: Cron expressions provide powerful scheduling capabilities for automated workflow execution
4. **HTTP Integration**: FastAPI bridges external systems with Temporal workflows through REST endpoints
5. **Event Aggregation**: Workflows can collect and process multiple external events before completing
6. **Graceful Control**: External systems can request workflow termination through signals
7. **Monitoring Integration**: Web UI provides comprehensive visibility into scheduled and triggered workflows

## 🔄 Next Steps

- **Experiment with Complex Schedules**: Try advanced cron expressions for specific business requirements
- **Build Webhook Handlers**: Integrate with external services like GitHub, Slack, or payment processors  
- **Implement Event Sourcing**: Use signals to build event-driven architectures
- **Scale Horizontally**: Deploy multiple worker instances for high-throughput scenarios
- **Add Authentication**: Secure API endpoints with proper authentication and authorization
- **Implement Monitoring**: Add metrics collection and alerting for production deployments

This lab demonstrates how Temporal seamlessly integrates with external systems, making it ideal for building robust, event-driven applications that span multiple services and time-based triggers.