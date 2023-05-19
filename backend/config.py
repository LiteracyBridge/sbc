import json
from typing import Any, Optional

from boto3 import Session
from dotenv import load_dotenv
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


class Settings:
    db_name: str
    db_host: str
    db_password: str
    db_user: str
    db_port: Optional[str] = "5432"

    is_local: bool = False

    def __init__(self) -> None:
        if getenv("APP_ENV", "production") == "local":
            load_dotenv()

            self.is_local = True
            self.db_name = getenv("DB_NAME", "impact")
            self.db_host = getenv("DB_HOST", "localhost")
            self.db_password = getenv("DB_PASSWORD", "")
            self.db_user = getenv("DB_USER", "postgres")
            self.db_port = getenv("DB_PORT", "5432")
        else:
            self.load_aws_secrets()

    def load_aws_secrets(self):
        # @classmethod
        session = Session()
        client = session.client(
            # endpoint_url="http://localhost:4566",
            service_name="secretsmanager",
            region_name=AWS_REGION,
        )
        secret_name: str = "lb_stats_test"
        # def _get_secret( secret_name: str) -> str | dict[str, Any]:
        try:
            secret_string = client.get_secret_value(SecretId=secret_name)[
                "SecretString"
            ]
            secrets = json.loads(secret_string)

            # secrets = self._get_secret("lb_stats_test")
            self.db_name = "impact"
            self.db_user = secrets["username"]
            self.db_password = secrets["password"]
            self.db_host = secrets["host"]
            self.db_port = secrets["port"]

        except Exception as err:
            raise err
            return secret_string

    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


    # @classmethod
    # def get_secrets(self, settings: BaseSettings) -> dict[str, Any]:

    # @classmethod
    # def customize_sources(
    #     cls,
    #     init_settings: SettingsSourceCallable,
    #     env_settings: SettingsSourceCallable,
    #     file_secret_settings: SettingsSourceCallable,
    # ):
    #     return (
    #         init_settings,
    #         cls.get_secrets,
    #         env_settings,
    #         file_secret_settings,
    #     )


# class Settings:
#     # example_secret: str
#     db_name: str
#     db_host: str
#     db_password: str
#     db_user: str
#     db_port: Optional[str] = "5432"
#     # db: DatabaseSettings

#     class Config(SecretManagerConfig):
#         if getenv("APP_ENV", "production") == "local":
#             env_file = ".env"
#         # ...


settings = Settings()
# print(Settings().db_password)
