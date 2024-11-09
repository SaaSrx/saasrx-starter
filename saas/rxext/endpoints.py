from collections import defaultdict
from typing import Any

from reflex.page import get_decorated_pages

FRONTEND_DECORATED_PAGES = get_decorated_pages()
API_DECORATED_PAGES: dict[str, list] = defaultdict(list)


def api(
    route: str,
    methods: list[str] = ["GET"],
    response_model: Any = None,
    status_code: int = 200,
    tags: list[str] = None,
    summary: str = None,
    description: str = None,
    response_description: str = "Successful Response",
    **kwargs,
):
    """Decorate a function as an API endpoint.

    To be used with:
        `app.api.add_api_route(path, endpoint, **options)`

    Args:
        route: The route to reach the API.
        methods: The HTTP methods allowed for the API.
        response_model: The response model for the API.
        status_code: The status code for the response.
        tags: Tags for the API.
        summary: Summary of the API.
        description: Description of the API.
        response_description: Description of the response.
        **kwargs: Additional keyword arguments.

    Returns:
        The decorated function.
    """

    def decorator(api_fn):
        API_DECORATED_PAGES[route].append(
            {
                **kwargs,
                "path": route,
                "endpoint": api_fn,
                "methods": methods,
                "response_model": response_model,
                "status_code": status_code,
                "tags": tags,
                "summary": summary,
                "description": description,
                "response_description": response_description,
            }
        )

        return api_fn

    return decorator


class RouteMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Create the new class
        cls = super().__new__(mcs, name, bases, attrs)

        # Initialize route parts list
        route_parts = []

        # Traverse the MRO in reverse to collect routes from base classes
        for base in cls.__mro__[::-1]:
            if hasattr(base, "route") and base.route:
                route_parts.append(base.route)

        # Build the endpoint path
        route = "/".join(route_parts)
        if not route.startswith("/"):
            route = "/" + route

        # Assign the route to the class
        cls.path = route

        return cls


class Endpoint(metaclass=RouteMeta):
    """Base class for API endpoints."""

    path: str
    route = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
