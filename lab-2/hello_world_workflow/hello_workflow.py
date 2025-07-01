from temporalio import workflow # type: ignore
from temporalio.common import RetryPolicy # type: ignore
from datetime import timedelta

# Import the activity
with workflow.unsafe.imports_passed_through():
    from hello_activity import say_hello

@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        # Extract 'name' from the input dictionary, default to "Unknown" if not found
        # name = input_data.get("name", "Unknown")
        return await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=5),
            retry_policy=RetryPolicy(maximum_attempts=2)
        )