from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "PhD Xpert Solver"
    DEBUG: bool = False
    ENV: str = "development"
    API_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    DATABASE_URL: str = "postgresql+asyncpg://phdxpert:phdxpert@localhost:5432/phdxpert"
    REDIS_URL: str = "redis://localhost:6379/0"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    NEO4J_URL: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "phdxpert"
    WEAVIATE_URL: str = "http://localhost:8080"
    JWT_SECRET: str = "super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 7
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    MICROSOFT_CLIENT_ID: Optional[str] = None
    MICROSOFT_CLIENT_SECRET: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_MODEL: str = "gemini-1.5-pro"
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    SHODAN_API_KEY: Optional[str] = None
    CENSYS_API_ID: Optional[str] = None
    CENSYS_API_SECRET: Optional[str] = None
    VIRUSTOTAL_API_KEY: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
