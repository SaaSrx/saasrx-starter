"""Generic API bootstrap system for Reflex applications."""

import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI, Request

from rxext.config import APIConfig
from rxext.console import debug, error, info, warn
from rxext.utils.exec_util import get_environment_info, is_prod_mode, is_testing_env


def load_routes_from_path(path: str, prefix: str = "/api", default_method: str = "GET") -> list[APIRouter]:
    """
    Auto-discover and load routes from Python files in a directory.

    For each .py file:
    1. If module has 'router' (APIRouter), include it directly
    2. Otherwise, create routes from callable functions

    Args:
        path: Directory path to scan for route files
        prefix: URL prefix for discovered routes
        default_method: Default HTTP method for function-based routes

    Returns:
        List of APIRouter instances
    """
    routers = []
    path_obj = Path(path)

    info(f"🔍 Looking for API routes in: {path}")

    if not path_obj.exists():
        warn(f"❌ Route path does not exist: {path}")
        return routers

    for py_file in path_obj.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue

        debug(f"📁 Found route file: {py_file.name}")

        # Calculate module path relative to the search path
        relative_path = py_file.relative_to(path_obj)
        module_parts = list(relative_path.parts[:-1]) + [relative_path.stem]

        try:
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location(".".join(module_parts), py_file)
            if not spec or not spec.loader:
                error(f"❌ Could not load spec for {py_file.name}")
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if module has a router
            if hasattr(module, "router") and isinstance(module.router, APIRouter):
                debug(f"✅ Found APIRouter in {py_file.name}")
                # Log the routes in the router
                for route in module.router.routes:
                    if hasattr(route, "path") and hasattr(route, "methods"):
                        methods = list(route.methods) if route.methods else ["GET"]
                        debug(f"   📍 {' '.join(methods)} {prefix}{route.path}")
                routers.append(module.router)
                continue

            # Otherwise, create router from callable functions
            router = APIRouter()
            route_added = False

            debug(f"🔧 Creating function-based routes for {py_file.name}")

            for name, obj in inspect.getmembers(module):
                if name.startswith("_") or not callable(obj) or inspect.isclass(obj) or inspect.isbuiltin(obj):
                    continue

                # Determine HTTP method
                method = getattr(obj, "http_method", default_method).upper()

                # Determine route path
                if hasattr(obj, "route_path"):
                    route_path = obj.route_path
                else:
                    # Build path from file structure
                    path_parts = list(relative_path.parts[:-1]) + [relative_path.stem]
                    route_path = "/" + "/".join(path_parts)

                # Add the route
                router.add_api_route(route_path, obj, methods=[method], name=f"{name}_{method.lower()}")
                debug(f"   📍 {method} {prefix}{route_path} -> {name}()")
                route_added = True

            if route_added:
                routers.append(router)
            else:
                warn(f"⚠️  No routes found in {py_file.name}")

        except Exception as e:
            # Log error but continue processing other files
            error(f"Warning: Failed to load routes from {py_file}: {e}")
            continue

    return routers


def create_api_app(config: APIConfig) -> FastAPI:
    """
    Create a FastAPI application with auto-loaded routes.

    Args:
        config: API configuration

    Returns:
        Configured FastAPI application
    """
    # Create FastAPI app with provided config
    app = FastAPI(**config.fastapi_kwargs)

    # Add default health endpoint if enabled
    if config.add_default_health:

        @app.get("/health")
        async def health_check(request: Request) -> dict[str, Any]:
            response = {"status": "ok"}

            if config.include_environment_info:
                response.update(get_environment_info())
                response["message"] = "API health check successful"

            if config.include_client_info and hasattr(request, "client"):
                response["client"] = str(request.client)

            return response

    # Load and include routers from configured paths
    total_routers = 0
    for route_path in config.route_paths:
        routers = load_routes_from_path(route_path, config.prefix, config.default_method)

        for router in routers:
            app.include_router(router, prefix=config.prefix)
            total_routers += 1

    info(f"🚀 API app created with {total_routers} routers")
    info(f"📋 API docs available at: {config.docs_url}")

    return app
