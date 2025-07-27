from .config import settings
from .utils import is_url, create_inline_keyboard, async_tempdir, similarity

TOKEN = settings.BOT_TOKEN
SP = settings.authorization

__all__ = [
    "TOKEN",
    "SP",
    "is_url",
    "create_inline_keyboard",
    "async_tempdir",
    "similarity"
]