import reflex as rx

from rxconfig import secrets
from saas.components import features, navbar


def pricing() -> rx.Component:
    return rx.box(rx.text("Pricing Section"), id="pricing")


def testimonials() -> rx.Component:
    return rx.box(rx.text("Testimonials Section"), id="testimonials")


def get_started() -> rx.Component:
    return rx.box(rx.text("Get Started Section"), id="get-started")


def index() -> rx.Component:
    """
    main index page.  can check status with
    secrets.status_mode
    """
    return rx.box(
        navbar.navbar(),
        features.features(),
        # rx.vstack(
        # rx.spacer(),
        #     rx.spacer(),
        #     pricing(),
        #     rx.spacer(),
        #     testimonials(),
        #     rx.spacer(),
        #     get_started(),
        # ),
        # class_name="min-h-screen bg-white",
    )


"""
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Rocket className="h-8 w-8 text-indigo-600" />
            <span className="ml-2 text-xl font-bold text-gray-900">
              ShipQuick
            </span>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-600 hover:text-gray-900">
              Feats
            </a>
            <a href="#pricing" className="text-gray-600 hover:text-gray-900">
              Pricing
            </a>
            <a
              href="#testimonials"
              className="text-gray-600 hover:text-gray-900"
            >
              Testimonials
            </a>
            <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors">
              Get Started
            </button>
          </div>

          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-600"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

"""
