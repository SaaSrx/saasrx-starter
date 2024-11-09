from fastapi import Request

from saas.rxext import console, is_prod_mode, is_testing_env

# Allows for either decorator or manual route addition, e.g.:
# @api("/health", methods=["GET"])
# or just add to the API_ROUTES lis


async def api_health(req: Request):
    console.log(f"[cyan]\[HEALTH][/cyan]\t{req.client=}")
    extra = {
        "message": "retrieved health check",
        "prod": is_prod_mode(),
        "testing_env": is_testing_env(),
        # other info
    }
    return {"status": "okay", **extra}
