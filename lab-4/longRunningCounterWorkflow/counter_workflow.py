from temporalio import workflow
from datetime import timedelta

@workflow.defn(name="CounterWorkflow")
class CounterWorkflow:
    def __init__(self):
        self.count = 0

    @workflow.run
    async def run(self) -> int:
        while True:
            await workflow.sleep(timedelta(seconds=10))
            if not workflow.unsafe.is_replaying():
                print(f"Current count (no signal): {self.count}")

    @workflow.signal
    async def increment(self) -> None:
        self.count += 1
        if not workflow.unsafe.is_replaying():
            print(f"Count incremented to: {self.count}")

    @workflow.query
    def get_count(self) -> int:
        return self.count