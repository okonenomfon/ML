from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Credit Risk Assessment API"
    api_version: str = "v1"
    debug: bool = False
    model_path: str = "models/credit_risk_model.pkl"
    features_path: str = "models/required_features.pkl"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
