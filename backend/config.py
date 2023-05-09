import json
from typing import Any

from boto3 import Session
from pydantic import BaseSettings, BaseModel
from pydantic.env_settings import SettingsSourceCallable
from os import getenv

AWS_REGION = "us-west-2"

# session = Session(
#     aws_access_key_id="test",
#     aws_secret_access_key="test",
#     region_name="us-east-1",
# )

# client = session.client(
#     endpoint_url="http://localhost:4566",
#     service_name="secretsmanager",
#     region_name="us-east-1",
# )


class SecretManagerConfig:
    def __init__(self) -> None:
        self.session = Session(
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
        )
        self.client = self.session.client(
            endpoint_url="http://localhost:4566",
            service_name="secretsmanager",
            region_name="us-east-1",
        )

    @classmethod
    def _get_secret(cls, secret_name: str) -> str | dict[str, Any]:
        secret_string = cls.client.get_secret_value(SecretId=secret_name)[
            "SecretString"
        ]
        try:
            return json.loads(secret_string)
        except json.decoder.JSONDecodeError:
            return secret_string

    @classmethod
    def get_secrets(cls, settings: BaseSettings) -> dict[str, Any]:
        return {db_name: cls._get_secret(name) for name, _ in settings.__fields__.items()}

    @classmethod
    def customize_sources(
        cls,
        init_settings: SettingsSourceCallable,
        env_settings: SettingsSourceCallable,
        file_secret_settings: SettingsSourceCallable,
    ):
        return (
            init_settings,
            cls.get_secrets,
            env_settings,
            file_secret_settings,
        )


class DatabaseSettings(BaseModel):
    user: str
    password: str
    db_name: str


class Settings(BaseSettings):
    # example_secret: str
    db_name: str
    db_host: str
    db_password: str
    db_user: str
    # db: DatabaseSettings

    class Config(SecretManagerConfig):
        if getenv("APP_ENV", "production") == "local":
            env_file = ".env"
        # ...


settings = Settings()
print(Settings().dict())
