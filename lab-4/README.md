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


