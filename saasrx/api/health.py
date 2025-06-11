from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health")
async def api_health():
    # Basic health check, can be expanded later
    return {"status": "ok", "message": "SaaSRX API is healthy"}
