import reflex as rx

from saasrx.routes import ROUTES


class State(rx.State):
    # redirect related
    redirect_cancel: bool = False
    redirect_timer_amt: int = 3
    _redirect_route: str = ROUTES.DASHBOARD
    # _redirect_task: asyncio.Task | None = None  # this doesnt work afaict
