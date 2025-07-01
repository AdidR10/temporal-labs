from temporalio import workflow # type: ignore
from temporalio.common import RetryPolicy # type: ignore
from datetime import timedelta

# Import the activity
with workflow.unsafe.imports_passed_through():
    from compose_greeting_activity import compose_greeting, ComposeGreetingInput

@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, input_data: dict) -> str:
        # By default activities will retry, backing off an initial interval and
        # then using a coefficient of 2 to increase the backoff each time after
        # for an unlimited amount of time and an unlimited number of attempts.
        # We'll keep those defaults except we'll set the maximum interval to
        # just 2 seconds.
        # @@@SNIPSTART python-activity-retry
        name = input_data.get("name", "Unknown")
        return await workflow.execute_activity(
            compose_greeting,
            ComposeGreetingInput("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_interval=timedelta(seconds=4)),
        )
        # @@@SNIPEND
