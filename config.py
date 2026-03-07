from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    database_url: str
    admin_id: int
    
    app_title: str = "Prive Club Sochi"
    web_app_url: str = "https://your-webapp-url.com"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
