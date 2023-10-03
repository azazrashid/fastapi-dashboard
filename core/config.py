from enum import Enum
from pydantic import BaseSettings


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    DATABASE_URL: str
    RELEASE_VERSION: str = "1.0"

    class Config:
        env_file = "./.env"


config: Config = Config()
