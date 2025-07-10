from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

# Import the activity
with workflow.unsafe.imports_passed_through():
    from hello_activity import say_hello

@workflow.defn
class HelloWorkflow:
    """
    Workflow that orchestrates the hello activity.
    Workflows are durable and can survive failures.
    """
    
    @workflow.run
    async def run(self, name: str) -> str:
        # Execute activity with timeout and retry policy
        return await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=2)
        )