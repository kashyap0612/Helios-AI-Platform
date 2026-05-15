from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Helios AI Platform'
    env: str = 'dev'
    log_level: str = 'INFO'
    redis_url: str = 'redis://redis:6379/0'
    postgres_url: str = 'postgresql+asyncpg://postgres:postgres@postgres:5432/helios'
    qdrant_url: str = 'http://qdrant:6333'
    vllm_small_model: str = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
    vllm_large_model: str = 'meta-llama/Llama-3.1-8B-Instruct'
    cache_ttl_sec: int = 900
    rate_limit_per_min: int = 60


settings = Settings()
