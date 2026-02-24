from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "NexusHR AI"
    DEBUG: bool = True
    MISTRAL_API_KEY: str
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="allow"  # Это разрешит "лишние" поля и уберет твою ошибку
    )


settings = Settings()