import reflex as rx

features_list = [
    {
        "name": "Lightning Fast Setup",
        "description": "Get your SaaS up and running in minutes with our pre-built components and templates.",
        "icon": "zap",
    },
    {
        "name": "Save Weeks of Development",
        "description": "Skip the boilerplate and focus on what makes your product unique.",
        "icon": "clock",
    },
    {
        "name": "Authentication Ready",
        "description": "Secure authentication system with social logins, ready out of the box.",
        "icon": "lock",
    },
    {
        "name": "Clean Code",
        "description": "Well-structured, documented code following best practices.",
        "icon": "code",
    },
    {
        "name": "Database Setup",
        "description": "Pre-configured database schemas and models for common use cases.",
        "icon": "database",
    },
    {
        "name": "Deploy Instantly",
        "description": "One-click deployment to your favorite cloud provider.",
        "icon": "cloud",
    },
]


def features() -> rx.Component:
    return rx.el.div(
        rx.box(
            rx.box(
                rx.heading(
                    "Features",
                    class_name="text-base text-indigo-600 font-semibold tracking-wide uppercase",
                ),
                rx.text(
                    "Everything you need to succeed",
                    class_name="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-indigo-900 sm:text-4xl",
                ),
                rx.text(
                    "Launch your SaaS product with confidence using our complete toolkit.",
                    class_name="mt-4 max-w-2xl text-xl text-indigo-600/80 lg:mx-auto",
                ),
                class_name="lg:text-center",
            ),
            rx.box(
                rx.box(
                    *[
                        rx.box(
                            rx.box(
                                rx.icon(
                                    feature["icon"],
                                    class_name="h-6 w-6 aria-hidden:true",
                                ),
                                class_name="absolute h-12 w-12 flex items-center justify-center rounded-md bg-indigo-600 text-white",
                            ),
                            rx.box(
                                rx.heading(
                                    feature["name"],
                                    level=3,
                                    class_name="text-lg font-medium text-indigo-900",
                                ),
                                rx.text(
                                    feature["description"],
                                    class_name="mt-2 text-base text-indigo-600/80",
                                ),
                                class_name="ml-16",
                            ),
                            class_name="relative",
                        )
                        for feature in features_list
                    ],
                    class_name="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-3",
                ),
                class_name="mt-20",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        id="features",
        class_name="py-24 bg-indigo-50/50",
    )
