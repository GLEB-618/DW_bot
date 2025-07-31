from .config import settings
from .utils import is_url, create_inline_keyboard, async_tempdir, similarity, is_spotify_url, extract_spotify_track_id

TOKEN = settings.BOT_TOKEN
SP = settings.authorization
HTTPS_PROXY = settings.HTTPS_PROXY

__all__ = [
    "TOKEN",
    "SP",
    "HTTPS_PROXY",
    "is_url",
    "create_inline_keyboard",
    "async_tempdir",
    "similarity",
    "is_spotify_url",
    "extract_spotify_track_id"
]