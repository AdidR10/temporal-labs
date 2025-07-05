import random
import time
from temporalio import activity
from typing import Optional
import asyncio

@activity.defn
async def unreliable_greeting_activity(name: str, failure_rate: float = 0.7) -> str:
    """
    An activity that simulates real-world failures.
    
    Args:
        name: The name to greet
        failure_rate: Probability of failure (0.0 to 1.0)
    
    Returns:
        A greeting message if successful
        
    Raises:
        Exception: Simulated transient failure
    """
    
    # Get activity info for logging
    info = activity.info()
    attempt = info.attempt
    
    print(f"🔄 Activity attempt #{attempt} for name: {name}")
    
    # Simulate network delay
    await asyncio.sleep(random.uniform(0.5, 2.0))
    
    # Simulate failures based on failure rate
    if random.random() < failure_rate:
        error_types = [
            "NetworkTimeoutError: Connection timed out",
            "ServiceUnavailableError: External service temporarily unavailable", 
            "RateLimitError: Rate limit exceeded, please retry later",
            "DatabaseConnectionError: Temporary database connection issue"
        ]
        error_message = random.choice(error_types)
        print(f"❌ Activity failed on attempt #{attempt}: {error_message}")
        raise Exception(f"Simulated failure: {error_message}")
    
    # Success case
    success_message = f"Hello, {name}! (Successful on attempt #{attempt})"
    print(f"✅ Activity succeeded on attempt #{attempt}")
    return success_message

@activity.defn 
async def slow_processing_activity(data: str, processing_time: int = 10) -> str:
    """
    An activity that takes a long time to complete (for timeout testing).
    
    Args:
        data: Data to process
        processing_time: Time in seconds to simulate processing
        
    Returns:
        Processed data result
    """
    
    info = activity.info()
    print(f"🐌 Starting slow processing activity (attempt #{info.attempt})")
    print(f"⏱️  Will take {processing_time} seconds to complete")
    
    # Simulate long-running processing
    for i in range(processing_time):
        await asyncio.sleep(1)
        print(f"⏳ Processing... {i+1}/{processing_time} seconds elapsed")
        
        # Send heartbeat to indicate activity is still alive
        activity.heartbeat(f"Processing step {i+1}/{processing_time}")
    
    result = f"Processed: {data} (completed after {processing_time}s)"
    print(f"✅ Slow processing completed: {result}")
    return result