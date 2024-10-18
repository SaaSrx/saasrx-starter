from enum import Enum

import reflex


def run_uvicorn_backend(host: str, port: int, loglevel: str | Enum):
    """Run the backend in development mode using Uvicorn.

    Args:
        host: The app host
        port: The app port
        loglevel: The log level.
    """
    import uvicorn

    # original uses reload_dirs = [get_config().app_name],
    config = reflex.config.get_config()

    uvicorn.run(
        app=f"{reflex.utils.exec.get_app_module()}.{reflex.constants.CompileVars.API}",
        host=host,
        port=port,
        log_level=loglevel.value,
        reload=True,
        reload_dirs=config.reload_dirs,
    )


def patch_reflex():
    """
    while I am patching to make reload_dirs work better, could maybe use
    inspect.stack() to check what function is calling it, and then patch
    Config.app_name to return dynamically based on that

    due to how reflex does hot-reload, not possible to patch get_config or other functions easily

    """

    reflex.utils.exec.run_uvicorn_backend = run_uvicorn_backend
