import reflex as rx


def payment_success() -> rx.Component:
    return rx.box(
        rx.box(
            rx.icon("circle-check", class_name="h-12 w-12 text-green-500"),
            rx.heading("Payment Successful!", class_name="mt-6 text-3xl font-extrabold text-indigo-800"),
            rx.text(
                "You can now access the app. Check your email for a link to sign in.",
                class_name="mt-4 text-lg",
            ),
            class_name="shadow-lg p-6 bg-white rounded-lg",
        ),
        # class_name="min-h-screen bg-gradient-to-b from-indigo-50 to-white flex items-center justify-center px-4",
        class_name="min-h-screen flex items-center justify-center",
    )
