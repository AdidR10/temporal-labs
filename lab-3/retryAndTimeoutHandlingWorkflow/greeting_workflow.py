from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from typing import Optional

# Import activities
with workflow.unsafe.imports_passed_through():
    from compose_greeting_activity import unreliable_greeting_activity, slow_processing_activity

@workflow.defn
class RetryAndTimeoutWorkflow:
    """
    Workflow demonstrating retry policies and timeout handling.
    
    This workflow showcases:
    - Automatic retry on transient failures
    - Exponential backoff strategies  
    - Maximum retry limits
    - Various timeout configurations
    """
    
    @workflow.run
    async def run(self, name: str, scenario: str = "retry_demo") -> str:
        """
        Run different failure handling scenarios.
        
        Args:
            name: Name for greeting
            scenario: Type of demo ("retry_demo", "timeout_demo", "heartbeat_demo")
        """
        
        if scenario == "retry_demo":
            return await self._retry_demonstration(name)
        elif scenario == "timeout_demo":
            return await self._timeout_demonstration(name)
        elif scenario == "heartbeat_demo":
            return await self._heartbeat_demonstration(name)
        else:
            return await self._comprehensive_demo(name)
    
    async def _retry_demonstration(self, name: str) -> str:
        """Demonstrate retry policies with an unreliable activity."""
        
        # Configure aggressive retry policy for demonstration
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),      # Start with 1s delay
            backoff_coefficient=2.0,                    # Double delay each time
            maximum_interval=timedelta(seconds=10),     # Max 10s between retries
            maximum_attempts=5,                         # Try up to 5 times
            non_retryable_error_types=["PermanentError"] # Don't retry these errors
        )
        
        try:
            result = await workflow.execute_activity(
                unreliable_greeting_activity,
                args=[name, 0.7],  # 70% failure rate
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy
            )
            return f"🎉 Retry Demo Success: {result}"
            
        except Exception as e:
            return f"❌ Retry Demo Failed after all attempts: {str(e)}"
    
    async def _timeout_demonstration(self, name: str) -> str:
        """Demonstrate timeout handling with a slow activity."""
        
        # Configure short timeout to trigger timeout behavior
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_attempts=3
        )
        
        try:
            result = await workflow.execute_activity(
                slow_processing_activity,
                args=[f"data_for_{name}", 15],  # 15 second processing time
                start_to_close_timeout=timedelta(seconds=8),  # But only 8s timeout
                retry_policy=retry_policy
            )
            return f"🎉 Timeout Demo Success: {result}"
            
        except Exception as e:
            return f"⏰ Timeout Demo Failed: {str(e)}"
    
    async def _heartbeat_demonstration(self, name: str) -> str:
        """Demonstrate heartbeat mechanism with long-running activity."""
        
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_attempts=2
        )
        
        try:
            result = await workflow.execute_activity(
                slow_processing_activity,
                args=[f"heartbeat_data_{name}", 8],  # 8 second processing
                start_to_close_timeout=timedelta(seconds=20),  # Generous timeout
                heartbeat_timeout=timedelta(seconds=3),        # Heartbeat every 3s
                retry_policy=retry_policy
            )
            return f"💓 Heartbeat Demo Success: {result}"
            
        except Exception as e:
            return f"💔 Heartbeat Demo Failed: {str(e)}"
    
    async def _comprehensive_demo(self, name: str) -> str:
        """Run multiple activities with different failure scenarios."""
        
        results = []
        
        # Activity 1: Quick retry demo
        quick_retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_attempts=3
        )
        
        try:
            result1 = await workflow.execute_activity(
                unreliable_greeting_activity,
                args=[f"{name}_quick", 0.9],  # 50% failure rate
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=quick_retry_policy
            )
            results.append(f"Quick Retry: {result1}")
        except Exception as e:
            results.append(f"Quick Retry Failed: {str(e)}")
        
        # Activity 2: Conservative processing
        conservative_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            backoff_coefficient=1.5,
            maximum_attempts=2
        )
        
        try:
            result2 = await workflow.execute_activity(
                slow_processing_activity,
                args=[f"conservative_{name}", 5],  # 5 second processing
                start_to_close_timeout=timedelta(seconds=15),
                retry_policy=conservative_policy
            )
            results.append(f"Conservative: {result2}")
        except Exception as e:
            results.append(f"Conservative Failed: {str(e)}")
        
        return " | ".join(results)