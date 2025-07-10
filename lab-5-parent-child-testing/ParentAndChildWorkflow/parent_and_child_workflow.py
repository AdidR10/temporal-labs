from temporalio import workflow

# Nested child workflow (grandchild)
@workflow.defn
class NestedChildWorkflow:
    @workflow.run
    async def run(self, value: int) -> int:
        # Just return the value incremented
        return value + 1

# Child workflow that starts a nested child workflow
@workflow.defn
class ChildWorkflow:
    @workflow.run
    async def run(self, value: int) -> int:
        # Start the nested child workflow
        nested_result = await workflow.execute_child_workflow(
            NestedChildWorkflow.run,
            value,
            id=f"nested-child-{value}",
            task_queue="parent-and-child-task-queue",
        )
        # Return the result from the nested child
        return nested_result * 2

# Parent workflow that starts the child workflow
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, value: int) -> int:
        # Start the child workflow
        child_result = await workflow.execute_child_workflow(
            ChildWorkflow.run,
            value,
            id=f"child-{value}",
            task_queue="parent-and-child-task-queue",
        )
        # Return the result from the child
        return child_result * 3