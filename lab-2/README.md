# Hello World Workflow with Temporal - Docker Setup

This project demonstrates how to create and run a basic "Hello World" workflow using Temporal, a durable workflow orchestration platform. The setup uses Docker Compose to run both the Temporal server and a Python worker in isolated containers.

## 🎯 Project Goals

- **Understand Workflow Basics**: Learn how Temporal workflows and activities work
- **Set up Temporal Workflow Environment**: Run Temporal server and worker via Docker Compose
- **Create Workflow Components**: Implement activity, workflow, and worker in Python
- **Run Worker**: Process workflows and activities in a container
- **Start Workflow via CLI**: Trigger workflow execution using Temporal CLI
- **Observe in Web UI**: Monitor workflow execution in the Temporal dashboard

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Docker**: Version 20.0+ 
- **Docker Compose**: Version 2.0+
- **Web Browser**: For accessing the Temporal Web UI

### Verify Prerequisites

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Verify Docker is running
docker ps
```

## 🚀 Quick Start

### 1. Create Project Directory

```bash
# Create project directory
mkdir temporal-hello-world
cd temporal-hello-world
```

### 2. Create Docker Compose File

Create a `docker-compose.yml` file with the following content:

```yaml
version: '3.8'

services:
  temporal:
    image: temporalio/admin-tools:latest
    ports:
      - "7233:7233"
      - "8233:8233"
    entrypoint: []
    command: ["temporal", "server", "start-dev", "--ui-port", "8233", "--ip", "0.0.0.0"]

  worker:
    build: ./hello_world_workflow
    volumes:
      - ./hello_world_workflow:/app
    depends_on:
      - temporal
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    command: ["python", "worker.py"]
```

### 3. Create Workflow Directory and Dockerfile

```bash
# Create directory for workflow code
mkdir -p hello_world_workflow
cd hello_world_workflow
```

Create a `Dockerfile` in the `hello_world_workflow` directory:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Temporal Python SDK
RUN pip install temporalio

# Copy the workflow code
COPY . .

# Keep container running for development
CMD ["tail", "-f", "/dev/null"]
```

### 4. Create Workflow Files

Inside the `hello_world_workflow` directory, create the following files:

#### hello_activity.py
```python
from temporalio import activity

@activity.defn
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"
```

#### hello_workflow.py
```python
from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

# Import the activity
with workflow.unsafe.imports_passed_through():
    from hello_activity import say_hello

@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=RetryPolicy(maximum_attempts=2)
        )
```

#### worker.py
```python
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
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
```

#### start_workflow.py (Optional)
```python
import asyncio
from temporalio.client import Client
from hello_workflow import HelloWorkflow

async def main():
    # Connect to Temporal server
    client = await Client.connect("temporal:7233", namespace="default")
    
    # Start the workflow
    result = await client.execute_workflow(
        HelloWorkflow.run,
        "World",
        id="hello-workflow-id",
        task_queue="hello-task-queue",
    )
    
    print(f"Workflow result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 5. Start Temporal Server and Worker

Navigate back to the root directory (`temporal-hello-world`) and start the services:

```bash
# Build and start both Temporal server and worker
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 6. Verify Installation

```bash
# Check if containers are running
docker-compose ps

# View server and worker logs
docker-compose logs -f
```

### 7. Start the Workflow Using CLI

Use the Temporal CLI inside the container to start the workflow:

```bash
# Start the workflow with CLI
docker-compose exec temporal temporal workflow start \
  --task-queue hello-task-queue \
  --type HelloWorkflow \
  --input '{"name": "World"}' \
  --workflow-id hello-workflow-id \
  --namespace default
```

Alternatively, if you created `start_workflow.py`, you can run:

```bash
# Run the starter script in the worker container
docker-compose exec worker python start_workflow.py
```

### 8. Access Web UI to Observe Workflow

Open your browser and navigate to: http://localhost:8233

You should see the Temporal Web UI dashboard with the workflow execution:

1. Navigate to Workflows
2. Select the default namespace
3. You should see a workflow with ID `hello-workflow-id`
4. Click on it to view execution details
5. Check Status: It should show as "Completed"
6. View Output: Look at the "Input & Results" tab to see "Hello, World!"

### 9. Verify Workflow Execution via CLI

```bash
# Check workflow status
docker-compose exec temporal temporal workflow show \
  --workflow-id hello-workflow-id \
  --namespace default

# Get workflow result
docker-compose exec temporal temporal workflow query \
  --workflow-id hello-workflow-id \
  --namespace default
```

## 📁 Project Structure

```
temporal-hello-world/
├── docker-compose.yml      # Docker Compose configuration
├── README.md              # This file
└── hello_world_workflow/
    ├── Dockerfile          # Dockerfile for worker container
    ├── hello_activity.py   # Activity definition
    ├── hello_workflow.py   # Workflow definition
    ├── worker.py          # Worker to process workflows
    └── start_workflow.py  # Optional script to start workflow
```

## 🔧 Configuration Details

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  temporal:
    image: temporalio/admin-tools:latest
    ports:
      - "7233:7233"
      - "8233:8233"
    entrypoint: []
    command: ["temporal", "server", "start-dev", "--ui-port", "8233", "--ip", "0.0.0.0"]

  worker:
    build: ./hello_world_workflow
    volumes:
      - ./hello_world_workflow:/app
    depends_on:
      - temporal
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
    command: ["python", "worker.py"]
```

### Configuration Breakdown

#### Temporal Service:
- **Image**: `temporalio/admin-tools:latest` - Official Temporal tools image with CLI included
- **Ports**:
  - 7233: Temporal Server API endpoint
  - 8233: Web UI dashboard
- **Entrypoint**: Cleared to override default behavior
- **Command**: Starts Temporal in development mode with Web UI

#### Worker Service:
- **Build**: Builds from local Dockerfile in `hello_world_workflow`
- **Volumes**: Mounts local code into container for live updates
- **Depends On**: Ensures Temporal server starts first
- **Environment**: Sets Temporal server address for worker connection
- **Command**: Runs the worker script to process workflows

### Why These Settings?
- `--ui-port 8233`: Specifies Web UI port for Temporal server
- `--ip 0.0.0.0`: Binds to all interfaces (required for Docker port mapping)
- `start-dev`: Uses in-memory database (perfect for learning)
- `TEMPORAL_ADDRESS=temporal:7233`: Directs worker to Temporal server within Docker network

## 🌐 Accessing Services

### Temporal Server
- **URL**: http://localhost:7233
- **Purpose**: API endpoint for workflow operations
- **Test**: `curl http://localhost:7233/api/v1/namespaces`

### Temporal Web UI
- **URL**: http://localhost:8233
- **Purpose**: Visual dashboard for monitoring workflows
- **Features**:
  - View workflow executions
  - Monitor task queues
  - Explore workflow history
  - Debug failed workflows

## 🏷 Workflow Components

### Overview of Files

| File | Purpose |
|------|---------|
| `hello_activity.py` | Defines the say_hello activity that returns a greeting |
| `hello_workflow.py` | Defines the HelloWorkflow workflow that calls the activity |
| `worker.py` | Runs a worker to process workflows and activities on the hello-task-queue |
| `start_workflow.py` | Optional script to start the workflow programmatically |

### How It Works
1. **Activity** (`say_hello`): A simple function that takes a name and returns a greeting.
2. **Workflow** (`HelloWorkflow`): Orchestrates the activity execution with retry policies and timeouts.
3. **Worker**: Listens on a task queue (`hello-task-queue`) for workflow and activity tasks to process.
4. **CLI Trigger**: Starts the workflow, passing input data (e.g., `name="World"`).

## 🔍 Exploring the Web UI

### Dashboard Overview
Navigate to http://localhost:8233
- Default view shows the namespace selector
- Key sections:
  - Workflows: View running and completed workflows
  - Task Queues: Monitor work distribution
  - Namespaces: Switch between different environments
  - Cluster: Server health and configuration

### Observing Your Workflow
1. Select Namespace: Choose default from the dropdown
2. View Workflows: Find `hello-workflow-id` in the list
3. Inspect Details: Click the workflow to see:
   - Execution history
   - Input (e.g., `{"name": "World"}`)
   - Result (e.g., "Hello, World!")
   - Timeline of events

### Web UI Features

#### Workflow Monitoring
- View workflow execution history
- Monitor workflow status and progress
- Inspect activity results and failures
- Trace workflow execution timeline

#### Task Queue Management
- Monitor task queue health (e.g., `hello-task-queue`)
- View pending and completed tasks
- Check worker connectivity
- Analyze task processing metrics

#### Namespace Management
- Switch between namespaces
- View namespace configuration
- Monitor namespace-specific metrics

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Container Won't Start
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs temporal
docker-compose logs worker

# Restart services
docker-compose restart
```

#### 2. Port Conflicts
If ports 7233 or 8233 are already in use:

```yaml
# Modify docker-compose.yml
ports:
  - "7234:7233"  # Use different host port
  - "8234:8233"  # Use different host port
```

Then restart:
```bash
docker-compose down
docker-compose up --build
```

#### 3. Web UI Not Accessible
```bash
# Verify container is running
docker ps

# Check if ports are mapped correctly
docker port $(docker-compose ps -q temporal)

# Test server connectivity
curl http://localhost:7233/api/v1/namespaces
```

#### 4. Worker Not Processing Workflows
```bash
# Check worker logs
docker-compose logs worker

# Ensure worker is running
docker-compose ps

# Restart worker if needed
docker-compose restart worker
```

#### 5. Workflow Not Starting
```bash
# Verify CLI command syntax
docker-compose exec temporal temporal workflow start \
  --task-queue hello-task-queue \
  --type HelloWorkflow \
  --input '{"name": "World"}' \
  --workflow-id hello-workflow-id \
  --namespace default

# Check if workflow appears in list
docker-compose exec temporal temporal workflow list --namespace default
```

### Debugging Commands
```bash
# Container status
docker-compose ps

# Server logs
docker-compose logs -f temporal

# Worker logs
docker-compose logs -f worker

# Execute into worker container
docker-compose exec worker bash

# Check server health
curl -s http://localhost:7233/api/v1/cluster/health
```

## 🧹 Cleanup

### Stop Services
```bash
# Stop containers
docker-compose down

# Stop and remove volumes (clears all data)
docker-compose down -v
```

### Remove Images
```bash
# Remove Temporal images
docker rmi temporalio/admin-tools:latest
docker rmi temporal-hello-world-worker

# Clean up unused images
docker system prune
```

## 📚 What's Next?

After completing this "Hello World" workflow, you can:

- **Enhance the Workflow**: Add more activities or complex logic to HelloWorkflow
- **Experiment with Policies**: Modify retry policies and timeouts in `hello_workflow.py`
- **Add Signals and Queries**: Enable dynamic interaction with running workflows
- **Build Real Applications**: Apply Temporal to real-world use cases like order processing
- **Production Setup**: Configure persistent databases (e.g., PostgreSQL) for durability

### Recommended Learning Path
1. ✅ Hello World Complete - Basic workflow running in Docker
2. 🔄 Advanced Workflow Features - Signals, queries, and child workflows
3. 📖 Error Handling - Learn about retries and compensation
4. 🏗️ Multi-Worker Applications - Scale with multiple workers and queues
5. 🚀 Production Deployment - Set up with persistent storage and monitoring

## 📖 Additional Resources

- [Official Documentation](https://docs.temporal.io/)
- [Temporal Samples](https://github.com/temporalio/samples-python)
- [Community Forum](https://community.temporal.io/)
- [GitHub Repository](https://github.com/temporalio/temporal)
- [Python SDK](https://github.com/temporalio/sdk-python)
- [Temporal Cloud](https://temporal.io/cloud)

## 🤝 Contributing

If you find issues or have improvements, please report them or suggest enhancements directly.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details if applicable, or refer to Temporal's official licensing.

