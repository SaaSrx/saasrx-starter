"""Example route demonstrating function-based API endpoint."""

async def get_example():
    """Simple example endpoint that will be available at /api/example"""
    return {"message": "Hello from auto-discovered route!", "path": "/api/example"}


async def custom_path_example():
    """Example with custom path override"""
    return {"message": "This route has a custom path", "actual_path": "/api/custom"}

# Override the default path for this function
custom_path_example.route_path = "/custom"


async def post_example():
    """Example POST endpoint"""
    return {"message": "POST endpoint example", "method": "POST"}

# Override the default method for this function
post_example.http_method = "POST"