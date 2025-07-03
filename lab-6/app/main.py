# api/main.py
from fastapi import FastAPI, HTTPException
from temporalio.client import Client
from cronWorkflow import CronWorkflow
from datetime import datetime

app = FastAPI()
client = None

@app.on_event("startup")
async def startup():
    import os
    global client
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")
    client = await Client.connect(temporal_address)

# ... rest of the API code remains the same

# 1. Regular HTTP trigger
@app.post("/trigger-workflow/{workflow_id}")
async def trigger_workflow(workflow_id: str, name: str = "HTTP Triggered"):
    """Trigger workflow from HTTP endpoint"""
    try:
        handle = await client.start_workflow(
            CronWorkflow.run,
            name,
            id=workflow_id,  
            task_queue="lab6-queue",
        )
        return {"workflow_id": handle.id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 2. Create cron schedule
@app.post("/schedule-workflow/{schedule_id}")
async def schedule_workflow(schedule_id: str, cron: str = "* * * * *"):
    """Schedule workflow with cron expression"""
    
    try:
        from datetime import datetime
        from temporalio.client import Schedule, ScheduleActionStartWorkflow, ScheduleSpec

        await client.create_schedule(
            schedule_id,
            Schedule(
                action=ScheduleActionStartWorkflow(
                    CronWorkflow.run,
                    "Cron Triggered",
                    id=f"cron-{datetime.now().timestamp()}",
                    task_queue="lab6-queue",
                ),
                spec=ScheduleSpec(
                    cron_expressions=[cron],
                ),
            ),
        )
        return {"schedule_id": schedule_id, "cron": cron, "status": "scheduled"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/schedule-workflow/{schedule_id}")
async def delete_schedule(schedule_id: str):
    """Delete (stop) a cron schedule"""
    try:
        handle = client.get_schedule_handle(schedule_id)
        await handle.delete()
        return {"schedule_id": schedule_id, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# 3. Signal workflow from external service
@app.post("/signal-workflow/{workflow_id}")
async def signal_workflow(workflow_id: str, message: str):
    """Send signal to running workflow"""
    try:
        handle = client.get_workflow_handle(workflow_id)
        await handle.signal(CronWorkflow.add_message, message)
        return {"workflow_id": workflow_id, "signal": "sent", "message": message}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/stop-workflow/{workflow_id}")
async def stop_workflow(workflow_id: str):
    """Send stop signal to workflow"""
    try:
        handle = client.get_workflow_handle(workflow_id)
        await handle.signal(CronWorkflow.stop_processing)
        return {"workflow_id": workflow_id, "signal": "stop sent"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/workflow-result/{workflow_id}")
async def get_result(workflow_id: str):
    """Get workflow result"""
    try:
        handle = client.get_workflow_handle(workflow_id)
        result = await handle.result()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))