from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from .activity import say_hello

@workflow.defn(name="CronWorkflow")
class CronWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        result = await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=5),
        )
        return f"Workflow completed with: {result}"

    @workflow.signal
    async def update_name(self, new_name: str):
        # Update the workflow state with a new name (example signal handler)
        await workflow.execute_activity(
            say_hello,
            new_name,
            start_to_close_timeout=timedelta(seconds=5),
        )