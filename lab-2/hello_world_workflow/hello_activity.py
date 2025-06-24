from temporalio import activity # type: ignore

@activity.defn
async def say_hello(name: str) -> str:
    return f"Hello, {name}!"