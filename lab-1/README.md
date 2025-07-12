# Lab 1: Introduction to Temporal

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- **Understand Temporal architecture**: Learn the core components and how they work together
- **Set up Temporal server**: Deploy Temporal using Docker Compose in Poridhi Lab
- **Explore the Web UI**: Navigate Temporal's dashboard and understand its features
- **Use Temporal CLI**: Execute commands to manage namespaces and server operations
- **Configure load balancers**: Set up external access for monitoring in Poridhi Lab
- **Work with namespaces**: Create and manage isolated environments for applications

## 📚 Background

### What is Temporal?
Temporal is an **open-source workflow orchestration platform** designed to build durable, scalable, and fault-tolerant applications. It enables developers to write complex business logic as workflows that can run for days, weeks, or even months, with built-in reliability features.

### Why Use Temporal?
- **Durability**: Workflows survive failures and restarts
- **Reliability**: Automatic retries and error handling
- **Scalability**: Distribute work across multiple workers
- **Visibility**: Rich monitoring and debugging capabilities
- **Simplicity**: Complex distributed logic written as simple code

### Core Architecture Components

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **Temporal Server** | Central orchestration engine | Stores workflow state, manages task queues |
| **Workflow** | Durable business logic | Defines process flow, handles failures |
| **Activity** | Individual task execution | Stateless operations, can be retried |
| **Worker** | Code execution environment | Polls for tasks, executes workflows/activities |
| **Web UI** | Monitoring dashboard | Visualize executions, debug issues |
| **CLI** | Command-line interface | Server management, namespace operations |

### Temporal Ecosystem Flow
1. **Client** starts a workflow
2. **Temporal Server** stores workflow state and creates tasks
3. **Worker** polls for tasks and executes workflow/activity code
4. **Web UI** provides visibility into all executions
5. **CLI** enables administrative operations

## 🛠 Prerequisites

### Poridhi Lab Environment:
- Access to Poridhi Lab with VS Code interface
- **Docker & Docker Compose**: ✅ Pre-installed in Poridhi Lab
- **Web Browser**: For accessing the Temporal Web UI through load balancer
- **Terminal Access**: Available through VS Code integrated terminal

### Verify Prerequisites
```bash
# Open VS Code terminal and verify Docker installation
docker --version
docker-compose --version
docker ps
```

## 📁 Project Structure

You'll create the following structure in your lab-1 directory:

```
lab-1/
├── docker-compose.yml      # Temporal server configuration
└── README.md              # This documentation
```

## 🚀 Lab Implementation

### Step 1: Set Up Project Structure

Open VS Code terminal in Poridhi Lab and navigate to your lab-1 directory:

```bash
# Navigate to lab-1 directory
cd lab-1

# Verify you're in the correct location
pwd
```

### Step 2: Create Docker Compose Configuration

Create `docker-compose.yml` in the lab-1 directory:

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
```

#### Configuration Explanation:
- **Image**: `temporalio/admin-tools:latest` - Includes Temporal server, CLI, and Web UI
- **Port 7233**: Temporal Server API endpoint for client connections
- **Port 8233**: Web UI dashboard for monitoring and debugging
- **start-dev**: Development mode with in-memory storage (perfect for learning)
- **--ip 0.0.0.0**: Binds to all interfaces for Docker networking

### Step 3: Deploy Temporal Server

```bash
# Start Temporal server
docker-compose up -d

# Verify container is running
docker-compose ps

# Check server logs
docker-compose logs -f temporal
```

Expected output: You should see Temporal server starting up with various initialization messages.

![make-up](./make-up.png?raw=true)


### Step 4: Configure Load Balancer for Web UI Access

#### Get Network Information
```bash
# Get your lab instance IP address
ifconfig eth0

# Note the IP address for load balancer configuration
```

#### Set Up Load Balancer
1. **Access Load Balancer Configuration** in Poridhi Lab interface
2. **Create New Load Balancer**:
   - **Enter IP**: Your lab instance eth0 IP address
   - **Enter Port**: `8233`
3. **Click Create**

You'll receive a load balancer URL like:
```
https://[your-instance-id]-lb-[port].bm-southeast.lab.poridhi.io/
```

### Step 5: Explore the Web UI

#### Access the Dashboard
1. **Open Temporal Web UI**: Use your load balancer URL in a web browser
2. **Explore the Interface**: You should see the Temporal dashboard with:
   - Namespace selector (default: "default")
   - Navigation sidebar with sections:
     - **Workflows**: View workflow executions
     - **Schedules**: Manage scheduled workflows
     - **Task Queues**: Monitor work distribution
     - **Cluster**: Server health and configuration

![dashboard](./dashboard.png?raw=true)

#### Dashboard Features

| Section | Purpose | What You'll See |
|---------|---------|-----------------|
| **Workflows** | Monitor workflow executions | Currently empty (no workflows yet) |
| **Task Queues** | View work distribution | Shows available task queues |
| **Namespaces** | Switch between environments | Default namespace pre-configured |
| **Cluster** | Server health monitoring | Server status and metrics |

### Step 6: Use Temporal CLI Commands

The Temporal CLI is included in the Docker container. Let's explore key commands:

#### Server Health Check
```bash
# Check if Temporal server is healthy
docker-compose exec temporal temporal server health

# Get server information
docker-compose exec temporal temporal cluster health
```

#### Namespace Operations

##### View Existing Namespaces
```bash
# List all namespaces
docker-compose exec temporal temporal namespace list

# Describe the default namespace
docker-compose exec temporal temporal namespace describe --namespace default
```

##### Create a New Namespace
```bash
# Register a new namespace for your application
docker-compose exec temporal temporal namespace register --namespace my-lab-app

# Register with retention period and description
docker-compose exec temporal temporal namespace register \
  --namespace production-app \
  --retention 72h \
  --description "Production application namespace"
```

##### Verify Namespace Creation
```bash
# List namespaces again to see your new ones
docker-compose exec temporal temporal namespace list

# Get details of your new namespace
docker-compose exec temporal temporal namespace describe --namespace my-lab-app
```

### Step 7: Explore Namespaces in Web UI

1. **Refresh Web UI**: Go back to your load balancer URL
2. **Switch Namespaces**: Use the namespace dropdown at the top
3. **Observe Changes**: Notice how you can now select different namespaces:
   - `default` (pre-existing)
   - `my-lab-app` (created by you)
   - `production-app` (if created)

### Step 8: Advanced CLI Exploration

#### Task Queue Operations
```bash
# List task queues (will be empty until workflows are running)
docker-compose exec temporal temporal task-queue list --namespace default

# Get task queue information
docker-compose exec temporal temporal task-queue describe \
  --task-queue sample-queue \
  --namespace default
```

#### Server Configuration
```bash
# View server configuration
docker-compose exec temporal temporal server config

# Check server version
docker-compose exec temporal temporal server --version
```

## 🔍 Understanding the System

### What You've Accomplished
1. **Deployed Temporal Server**: Running in development mode with in-memory storage
2. **Configured External Access**: Load balancer provides web access
3. **Explored Web UI**: Learned about monitoring capabilities
4. **Used CLI Tools**: Managed namespaces and server operations
5. **Created Isolation**: Set up separate namespaces for different applications

### System Architecture in Your Lab

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Load Balancer   │    │  Temporal       │
│                 │◄──►│                  │◄──►│  Server         │
│  (Your Computer)│    │  (Poridhi Lab)   │    │  (Docker)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Namespaces    │
                                               │  - default      │
                                               │  - my-lab-app   │
                                               │  - production.. │
                                               └─────────────────┘
```

### Key Concepts Demonstrated

#### Namespaces
- **Purpose**: Provide isolation between different applications or environments
- **Benefits**: Separate development, staging, and production workflows
- **Usage**: Switch between namespaces in Web UI or CLI

#### Development Mode
- **Storage**: In-memory (data lost on restart)
- **Purpose**: Fast setup for learning and development
- **Limitation**: Not suitable for production (use persistent storage)

## 🧪 Experimentation

### Try These Activities

#### 1. Create Multiple Namespaces
```bash
# Create namespaces for different environments
docker-compose exec temporal temporal namespace register --namespace development
docker-compose exec temporal temporal namespace register --namespace staging
docker-compose exec temporal temporal namespace register --namespace testing
```

#### 2. Namespace Management
```bash
# Update namespace retention
docker-compose exec temporal temporal namespace update \
  --namespace my-lab-app \
  --retention 168h

# Add description to existing namespace
docker-compose exec temporal temporal namespace update \
  --namespace development \
  --description "Development environment for testing workflows"
```

#### 3. Explore Different Web UI Sections
- Switch between namespaces and observe how the view changes
- Check the Cluster section for server metrics
- Explore the empty Workflows section (you'll fill this in later labs)
