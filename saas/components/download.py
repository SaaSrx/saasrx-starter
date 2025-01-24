import reflex as rx

from saas.state import DownloadState


def download_image(image_url: str = "/favicon.ico") -> rx.Component:
    # Button to use to test if download is working
    return rx.button("zip", on_click=rx.download(url=image_url))


def download_release() -> rx.Component:
    return rx.box(
        rx.button("zip", on_click=DownloadState.download_release),
    )
