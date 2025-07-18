from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    database_url: str
    check_gifts_delay_seconds: int

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
