# shared/workflow.py
from datetime import timedelta
from temporalio import workflow

@workflow.defn
class CronWorkflow:  # Better name - describes what it does
    def __init__(self):
        self.messages = []
        self.should_stop = False
    
    @workflow.signal
    async def add_message(self, message: str):
        """External services can send data via this signal"""
        self.messages.append(message)
    
    @workflow.signal  
    async def stop_processing(self):
        """External services can stop the workflow"""
        self.should_stop = True
    
    @workflow.run
    async def run(self, task_name: str) -> dict:
        """
        This workflow can be:
        1. Scheduled with cron (e.g., daily at 9am)
        2. Triggered manually via HTTP
        3. Receive signals while running
        """
        workflow.logger.info(f"Processing task: {task_name}")
        
        # Wait for signals or timeout
        await workflow.wait_condition(
            lambda: self.should_stop or len(self.messages) >= 5,
            timeout=timedelta(seconds=30)
        )   
        
        # Process collected messages
        processed_count = len(self.messages)
        
        return {
            "task": task_name,
            "messages_processed": processed_count,
            "messages": self.messages,
            "completed_at": str(workflow.now())
        }