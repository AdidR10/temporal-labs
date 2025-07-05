from temporalio import workflow
import asyncio
import logging
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError
# Define the child workflow
@workflow.defn
class ChildWorkflow:
    @workflow.run
    async def run(self, value: int) -> int:
        # Simulate partial failure for demonstration
        if value % 2 == 0:
            # raise Exception(f"Simulated failure for value {value}")
            raise ApplicationError(f"Simulated failure for value {value}")
        return value * 2

# Define the parent workflow
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, values: list[int]) -> list[int]:
        results = []
        child_futures = []
        # Start all child workflows in parallel
        for v in values:
            child_futures.append(
                workflow.execute_child_workflow(
                    ChildWorkflow.run,
                    v,
                    id=f"child-{v}",
                    retry_policy=RetryPolicy(maximum_attempts=1)  # disables retries
                )
            )
        # Wait for all child workflows to complete, handle failures gracefully
        completed = await asyncio.gather(*child_futures, return_exceptions=True)
        for idx, result in enumerate(completed):
            if isinstance(result, Exception):
                logging.error(f"Child workflow for value {values[idx]} failed: {result}")
                # Optionally, append a default value or skip
            else:
                #ADDRESS LATER: why logging.info is not showing any worker logs? For now, use print()
                print(f"Child workflow for value {values[idx]} completed with result: {result}")
                results.append(result)
        return results