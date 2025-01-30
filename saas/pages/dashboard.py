import reflex as rx

from saas.components import navbar
from saas.models import Payment, User
from saas.state.state import require_login, AuthState


def user_info_card(user: User) -> rx.Component:
    """Display user information in a card format."""
    return rx.vstack(
        rx.heading("User Profile", size="6", mb=4),
        rx.hstack(
            rx.text("Email:", font_weight="bold"),
            rx.text(user.email),
            width="100%",
        ),
        rx.hstack(
            rx.text("Access Level:", font_weight="bold"),
            rx.text(user.access_level.value),
            width="100%",
        ),
        rx.hstack(
            rx.text("Admin Status:", font_weight="bold"),
            rx.text("Yes" if user.is_admin else "No"),
            width="100%",
        ),
        padding="1em",
        bg="white",
        border_radius="lg",
        border="1px solid",
        border_color="gray.200",
        width="100%",
        align_items="start",
    )


def payment_history_card(payments: list[Payment]) -> rx.Component:
    """Display payment history in a card format."""
    return rx.vstack(
        rx.heading("Payment History", size="6", mb=4),
        rx.cond(
            len(payments) > 0,
            rx.vstack(
                *[
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                f"Amount: ${payment.amount/100:.2f}",
                                font_weight="bold",
                            ),
                            rx.text(f"Status: {payment.status}"),
                            rx.text(
                                f"Date: {payment.created.strftime('%Y-%m-%d %H:%M')}",
                                color="gray.600",
                            ),
                            align_items="start",
                        ),
                        width="100%",
                        padding="0.5em",
                        border_bottom="1px solid",
                        border_color="gray.100",
                    )
                    for payment in payments
                ],
                width="100%",
            ),
            rx.text("No payment history available.", color="gray.500"),
        ),
        padding="1em",
        bg="white",
        border_radius="lg",
        border="1px solid",
        border_color="gray.200",
        width="100%",
        align_items="start",
    )


def dashboard_user_info() -> rx.Component:
    return rx.vstack(
        rx.heading(
            "User Info",
            class_name="text-base text-indigo-600 font-semibold tracking-wide uppercase mb-2",
        ),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("Email:", font_weight="bold", min_width="100px"),
                    rx.text(AuthState.user.email),
                    class_name="w-full bg-gray-100 p-2 rounded-md",
                ),
                rx.hstack(
                    rx.text("Access Level:", class_name="font-bold min-w-[100px]"),
                    rx.text(AuthState.user.access_level),
                    class_name="w-full bg-white p-2 rounded-md",
                ),
                rx.hstack(
                    rx.text("Is Admin:", class_name="font-bold min-w-[100px]"),
                    rx.cond(AuthState.is_admin, "Yes", "No"),
                    class_name="w-full bg-gray-50 p-2 rounded-md",
                ),
                class_name="space-y-0 border border-gray-200 rounded-lg overflow-hidden",
                # class_name="border border-gray-200 rounded-lg overflow-hidden",
            ),
        ),
        align_items="stretch",
        width="100%",
        max_width="600px",
    )


def dashboard_contents() -> rx.Component:
    return rx.flex(
        rx.box(dashboard_user_info()),
        justify="center",
        class_name="bg-indigo-50/50",
    )


@navbar.for_page
@require_login
def dashboard_page() -> rx.Component:
    """The dashboard page."""
    return dashboard_contents()
