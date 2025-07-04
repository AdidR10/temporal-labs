from temporalio import activity

@activity.defn
async def say_hello(name: str) -> str:
    """
    Activity that generates a greeting message.
    Activities are where you put your business logic.
    """
    return f"Hello, {name}!"