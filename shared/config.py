from pydantic_settings import BaseSettings, SettingsConfigDict
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

class Settings(BaseSettings):
    BOT_TOKEN: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    PROXY_USER: str
    PROXY_PASS: str
    PROXY_HOST: str

    @property
    def authorization(self):
        proxies = {
            "http":  f"http://{self.PROXY_USER}:{self.PROXY_PASS}@{self.PROXY_HOST}",
            "https": f"http://{self.PROXY_USER}:{self.PROXY_PASS}@{self.PROXY_HOST}"
        }

        return Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=self.CLIENT_ID,
                client_secret=self.CLIENT_SECRET),
            proxies=proxies
        )

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore