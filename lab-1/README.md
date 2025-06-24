# Temporal Lab for Beginners

## Introduction to Temporal

Temporal is an open-source workflow orchestration platform designed to build and manage durable, scalable, and fault-tolerant applications. It allows developers to write complex business logic as workflows that can span days, weeks, or even months, with built-in features like retries, timeouts, and state management. Temporal is particularly useful for microservices, serverless architectures, and long-running processes.

### Three Basic Components of Temporal
1. **Workflow**: The core unit of execution that defines the business logic and sequence of tasks. Workflows are durable, meaning their state is preserved and can be recovered even if a process fails.
2. **Activity**: Individual tasks or units of work within a workflow, such as calling an API, processing data, or sending an email. Activities are executed by workers and can be retried if they fail.
3. **Worker**: A process that runs workflow and activity code, polling the Temporal Server for tasks and executing them. Workers are typically written using a Temporal SDK (e.g., in Go, Java, or Python).

Understanding these components is key to leveraging Temporal’s architecture. This lab will help you set up a basic Temporal environment and explore its features.

## Lab Goals
The purpose of this lab is to:
- Understand Temporal's architecture and its basic components.
- Set up a Temporal Server using Docker Compose.
- Explore the Web UI at `localhost:8233`.
- Register a namespace using the Temporal CLI.

This simple lab uses only the `temporalio/admin-tools` Docker image, which includes the Temporal Server, CLI commands, and a minimal functioning Web UI, making it ideal for beginners without the complexity of additional databases or services.


# Introduction to Temporal - Docker Setup

This project demonstrates how to set up and explore Temporal's workflow orchestration platform using Docker Compose. Temporal is a durable workflow execution platform that helps build reliable distributed applications.


## 🚀 Quick Start

### Create Docker Compose File

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
```

### Start Temporal Server

```bash
# Start Temporal using Docker Compose
docker-compose up

# Or run in background
docker-compose up -d
```


### Access Web UI

Open your browser and navigate to:
http://localhost:8233

You should see the Temporal Web UI dashboard.

## 📁 Project Structure

```
temporal-docker-setup/
├── docker-compose.yml      # Docker Compose configuration
├── README.md              # This file
└── examples/              # Sample workflows (optional)
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
```

### Configuration Breakdown:

- **Image**: `temporalio/admin-tools:latest` - Official Temporal tools image with CLI included
- **Ports**:
  - `7233`: Temporal Server API endpoint
  - `8233`: Web UI dashboard
- **Entrypoint**: Cleared to override default behavior
- **Command**: Starts Temporal in development mode with Web UI

### Why These Settings?

- `--ui-port 8233`: Specifies Web UI port
- `--ip 0.0.0.0`: Binds to all interfaces (required for Docker port mapping)
- `start-dev`: Uses in-memory database (perfect for learning)

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

## 🏷 Working with Namespaces

Namespaces provide isolation for different environments or applications. The Temporal CLI is already included in the Docker container.

### View Default Namespace

```bash
# List all namespaces
docker-compose exec temporal temporal namespace list

# Describe the default namespace
docker-compose exec temporal temporal namespace describe --namespace default
```

### Register a New Namespace

```bash
# Register a new namespace
docker-compose exec temporal temporal namespace register --namespace my-app

# Register with retention period
docker-compose exec temporal temporal namespace register \
  --namespace my-app \
  --retention 72h \
  --description "My application namespace"
```

### Namespace Operations

```bash
# List all namespaces
docker-compose exec temporal temporal namespace list

# Get namespace details
docker-compose exec temporal temporal namespace describe --namespace my-app

# Update namespace retention
docker-compose exec temporal temporal namespace update \
  --namespace my-app \
  --retention 168h
```

## 🔍 Exploring the Web UI

### Dashboard Overview

Navigate to http://localhost:8233
Default view shows the namespace selector

**Key sections**:
- Workflows: View running and completed workflows
- Task Queues: Monitor work distribution
- Namespaces: Switch between different environments
- Cluster: Server health and configuration

### Web UI Features

#### Workflow Monitoring
- View workflow execution history
- Monitor workflow status and progress
- Inspect activity results and failures
- Trace workflow execution timeline

#### Task Queue Management
- Monitor task queue health
- View pending and completed tasks
- Check worker connectivity
- Analyze task processing metrics

#### Namespace Management
- Switch between namespaces
- View namespace configuration
- Monitor namespace-specific metrics

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Container Won't Start

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs
```

🧹 Cleanup
Stop Services
# Stop containers
docker-compose down

# Stop and remove volumes (clears all data)
docker-compose down -v

Remove Images
# Remove Temporal images
docker rmi temporalio/admin-tools:latest

# Clean up unused images
docker system prune

📚 What's Next?
After completing this setup, you can:

Create your first workflow using Python, Go, or Java SDK
Build activities to handle business logic
Implement error handling and retry policies
Explore advanced features like signals, queries, and timers
Set up production deployment with persistent databases

Recommended Learning Path

✅ Setup Complete - Temporal running in Docker
🔄 SDK Tutorial - Choose your language and build workflows
📖 Core Concepts - Learn about durability and reliability
🏗️ Build Applications - Create real-world workflow examples
🚀 Production Setup - Configure with PostgreSQL/MySQL

📖 Additional Resources

Official Documentation
Temporal Samples
Community Forum
GitHub Repository
Python SDK
Temporal Cloud

🤝 Contributing
If you find issues or have improvements, please report them or suggest enhancements directly.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details if applicable, or refer to Temporal's official licensing.
