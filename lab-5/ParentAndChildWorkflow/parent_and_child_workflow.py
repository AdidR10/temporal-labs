# from temporalio import workflow
# import asyncio
# import logging
# from temporalio.common import RetryPolicy
# from temporalio.exceptions import ApplicationError
# # Define the child workflow
# @workflow.defn
# class ChildWorkflow:
#     @workflow.run
#     async def run(self, value: int) -> int:
#         # Simulate partial failure for demonstration
#         if value % 2 == 0:
#             # raise Exception(f"Simulated failure for value {value}")
#             raise ApplicationError(f"Simulated failure for value {value}")
#         return value * 2

# # Define the parent workflow
# @workflow.defn
# class ParentWorkflow:
#     @workflow.run
#     async def run(self, values: list[int]) -> list[int]:
#         results = []
#         child_futures = []
#         # Start all child workflows in parallel
#         for v in values:
#             child_futures.append(
#                 workflow.execute_child_workflow(
#                     ChildWorkflow.run,
#                     v,
#                     id=f"child-{v}",
#                     retry_policy=RetryPolicy(maximum_attempts=1)  # disables retries
#                 )
#             )
#         # Wait for all child workflows to complete, handle failures gracefully
#         completed = await asyncio.gather(*child_futures, return_exceptions=True)
#         for idx, result in enumerate(completed):
#             if isinstance(result, Exception):
#                 logging.error(f"Child workflow for value {values[idx]} failed: {result}")
#                 # Optionally, append a default value or skip
#             else:
#                 #ADDRESS LATER: why logging.info is not showing any worker logs? For now, use print()
#                 print(f"Child workflow for value {values[idx]} completed with result: {result}")
#                 results.append(result)
#         return results



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
        """
        Child workflow that processes a single value.
        Simulates failures for even numbers to demonstrate error handling.
        """
        # Simulate partial failure for demonstration
        if value % 2 == 0:
            raise ApplicationError(f"Simulated failure for value {value}")
        
        # Process the value (double it)
        result = value * 2
        workflow.logger.info(f"Child workflow processed {value} -> {result}")
        return result

# Define the parent workflow  
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, values: list[int]) -> dict:
        """
        Parent workflow that orchestrates multiple child workflows in parallel.
        Demonstrates fan-out/fan-in pattern with graceful error handling.
        """
        workflow.logger.info(f"Parent workflow starting with values: {values}")
        
        results = []
        errors = []
        child_futures = []
        
        # Start all child workflows in parallel (Fan-Out)
        for v in values:
            child_future = workflow.execute_child_workflow(
                ChildWorkflow.run,
                v,
                id=f"child-{v}",  # Unique child workflow ID
                retry_policy=RetryPolicy(maximum_attempts=1)  # Disable retries for demo
            )
            child_futures.append((v, child_future))
        
        # Wait for all child workflows to complete (Fan-In)
        completed = await asyncio.gather(
            *[future for _, future in child_futures], 
            return_exceptions=True  # Don't fail parent if children fail
        )
        
        # Process results and handle failures gracefully
        for idx, (original_value, _) in enumerate(child_futures):
            result = completed[idx]
            
            if isinstance(result, Exception):
                error_info = {
                    "value": original_value,
                    "error": str(result),
                    "type": type(result).__name__
                }
                errors.append(error_info)
                workflow.logger.error(f"Child workflow for value {original_value} failed: {result}")
            else:
                success_info = {
                    "value": original_value,
                    "result": result
                }
                results.append(success_info)
                workflow.logger.info(f"Child workflow for value {original_value} succeeded: {result}")
        
        # Return comprehensive results
        return {
            "total_children": len(values),
            "successful_results": results,
            "failed_children": errors,
            "success_count": len(results),
            "failure_count": len(errors),
            "success_rate": len(results) / len(values) if values else 0
        }