import asyncio
from temporalio import activity

@activity.defn
async def say_hello(name: str) -> str:
    """
    Activity that generates a greeting message.
    Activities are where you put your business logic.
    """
    
    # Wait for 10 seconds to simulate long-running activity
    await asyncio.sleep(20)
    
    return f"Hello, {name}!"