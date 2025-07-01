import os
import time
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from temporalio.client import Client
from CronWorkflow import CronWorkflow

temporal_client = None

async def connect_with_retry(address: str, max_retries: int = 10, delay: int = 5):
    """Connect to Temporal with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"API: Attempting to connect to Temporal at {address} (attempt {attempt + 1}/{max_retries})")
            client = await Client.connect(address)
            print("API: Successfully connected to Temporal!")
            return client
        except Exception as e:
            print(f"API: Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"API: Waiting {delay} seconds before retrying...")
                await asyncio.sleep(delay)
            else:
                raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global temporal_client
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    temporal_client = await connect_with_retry(temporal_address)
    
    yield
    
    # Shutdown (if needed)
    if temporal_client:
        await temporal_client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Temporal Cron Workflow API is running!"}

# HTTP endpoint to start the cron workflow
@app.post("/start-workflow/")
async def start_workflow(name: str):
    if not temporal_client:
        raise HTTPException(status_code=500, detail="Temporal client not initialized")
    
    workflow_id = f"cron-workflow-{name}"
    result = await temporal_client.execute_workflow(
        CronWorkflow.run,
        "Adid",
        id=workflow_id,
        task_queue=os.getenv("TASK_QUEUE", "cron-task-queue"),
        cron_schedule="* * * * *"  # Runs every minute
    )
    return {"message": f"Workflow started with ID: {workflow_id}", "result": str(result)}

# HTTP endpoint to signal the workflow
@app.post("/signal-workflow/")
async def signal_workflow(workflow_id: str, new_name: str):
    if not temporal_client:
        raise HTTPException(status_code=500, detail="Temporal client not initialized")
    
    handle = temporal_client.get_workflow_handle(workflow_id)
    await handle.signal(CronWorkflow.update_name, new_name)
    return {"message": f"Sent signal to workflow {workflow_id} with new name: {new_name}"}