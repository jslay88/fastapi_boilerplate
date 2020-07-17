from pydantic import BaseSettings


class Settings(BaseSettings):
    AUTH_ENABLED = True


settings = Settings()
