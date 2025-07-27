from .router import setup


def setup_all_routers(router):
    setup(router)

__all__ = [
    "setup_all_routers"
]