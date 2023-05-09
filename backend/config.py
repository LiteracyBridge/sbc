import json
from typing import Any, Optional

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
        self.session = Session()
        self.client = self.session.client(
            # endpoint_url="http://localhost:4566",
            service_name="secretsmanager",
            region_name=AWS_REGION,
        )
        self.secret_name: str = "lb_stats_test"

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
        secrets = cls._get_secret(cls.secret_name)
        return Settings(
            **{
                "db_name": "image",
                "db_password": secrets["password"],
                "db_host": secrets["host"],
                "db_port": secrets["port"],
            }
        )

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
    db_port: Optional[str] = "5432"
    # db: DatabaseSettings

    class Config(SecretManagerConfig):
        if getenv("APP_ENV", "production") == "local":
            env_file = ".env"
        # ...


settings = Settings()
# print(Settings().dict())
