from fastapi import APIRouter, Request

from rxext.utils.exec_util import get_environment_info

router = APIRouter()

@router.get("/health")
async def api_health(request: Request):
    """Enhanced health check with environment and client information."""
    response = {
        "status": "ok", 
        "message": "SaaSRX API is healthy"
    }
    
    # Add environment information
    response.update(get_environment_info())
    
    # Add client information if available
    if hasattr(request, 'client') and request.client:
        response["client"] = str(request.client)
    
    return response