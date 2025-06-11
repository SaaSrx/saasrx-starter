from fastapi import FastAPI
from .routes import api_router_v1  # Importing the main v1 router


def create_api_app(fastapi_app: FastAPI) -> FastAPI:
    """
    API transformer function to integrate the FastAPI router with Reflex.

    Args:
        fastapi_app: The FastAPI app instance provided by Reflex.

    Returns:
        The modified FastAPI app with included routers.
    """

    # Include the v1 router into the main FastAPI app
    fastapi_app.include_router(api_router_v1)

    # You can add other global API configurations here if needed,
    # such as middleware, exception handlers, etc.
    # Example:
    # from fastapi.middleware.cors import CORSMiddleware
    # fastapi_app.add_middleware(
    # CORSMiddleware,
    # allow_origins=["*"], # Adjust in production
    # allow_credentials=True,
    # allow_methods=["*"], # Adjust as needed
    # allow_headers=["*"], # Adjust as needed
    # )

    return fastapi_app
