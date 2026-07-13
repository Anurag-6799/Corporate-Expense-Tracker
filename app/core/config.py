from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    DATABASE_URL: str
    
    # Security Configurations (We will use these later for JWTs)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # This tells Pydantic to look for a file named .env in the root directory
    model_config = SettingsConfigDict(env_file=".env")

# We instantiate this exactly once. All other files will import this 'settings' object.
settings = Settings()