# Lab 5: Child Workflows & Parallel Tasks

**Goal:** Compose workflows using parent and child workflows with parallel execution and graceful failure handling.

## Features
- Define parent and child workflows
- Use `await asyncio.gather(...)` to run children concurrently
- Simulate partial failure and handle gracefully
- Retry policy configuration

## Quick Start

1. **Start Services:**
   ```bash
   docker-compose up --build
   ```

2. **Run Workflow:**
   ```bash
   docker-compose exec worker python start_workflow.py
   ```

3. **Access Temporal Web UI:**
   Open [http://localhost:8233](http://localhost:8233)

## How it Works
- Parent workflow spawns multiple child workflows in parallel
- Child workflows simulate failures for even numbers
- Parent workflow handles failures gracefully using `asyncio.gather(return_exceptions=True)`
- Failed children are logged but don't stop other children from completing

