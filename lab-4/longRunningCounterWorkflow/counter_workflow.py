from temporalio import workflow
from datetime import timedelta

@workflow.defn(name="CounterWorkflow")
class CounterWorkflow:
    def __init__(self):
        self.count = 0

    @workflow.run
    async def run(self) -> int:
        """
        Long-running workflow that maintains state and responds to signals.
        This workflow runs indefinitely, demonstrating persistent state management.
        """
        while True:
            # Sleep for 10 seconds between status updates
            await workflow.sleep(timedelta(seconds=10))
            
            # Print current status (only when not replaying)
            if not workflow.unsafe.is_replaying():
                print(f"Current count: {self.count}")

    @workflow.signal
    async def increment(self) -> None:
        """
        Signal handler to increment the counter.
        Signals allow external systems to send data to running workflows.
        """
        self.count += 1
        if not workflow.unsafe.is_replaying():
            print(f"🔔 Signal received! Count incremented to: {self.count}")

    @workflow.query
    def get_count(self) -> int:
        """
        Query handler to retrieve current counter value.
        Queries allow external systems to read workflow state without modification.
        """
        return self.count