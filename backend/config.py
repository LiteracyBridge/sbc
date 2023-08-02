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
    open_ai_key: Optional[str] = None
    user_pool_id: Optional[str] = None
    user_pool_client_id: Optional[str] = None

    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_whatapp_number: Optional[str] = None
    twilio_sms_number: Optional[str] = None

    sentry_dsn: Optional[str] = None

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
            self.sentry_dsn = getenv("SENTRY_DSN", None)
            self.open_ai_key = getenv("OPEN_AI_KEY", None)

            self.user_pool_id = getenv("AWS_USER_POOL_ID", None)
            self.user_pool_client_id = getenv("AWS_USER_POOL_CLIENT_ID", None)

            self.twilio_account_sid = getenv("TWILIO_ACCOUNT_SID", None)
            self.twilio_auth_token = getenv("TWILIO_AUTH_TOKEN", None)
            self.twilio_whatapp_number = getenv("TWILIO_WHATSAPP_NUMBER", None)
            self.twilio_sms_number = getenv("TWILIO_SMS_NUMBER", None)
        else:
            self.load_aws_secrets()

    def load_aws_secrets(self):
        session = Session()
        client = session.client(
            # endpoint_url="http://localhost:4566",
            service_name="secretsmanager",
            region_name=AWS_REGION,
        )
        try:
            # Load postgres secrets
            secret_string = client.get_secret_value(SecretId="lb_stats_test")[
                "SecretString"
            ]
            secrets = json.loads(secret_string)

            # secrets = self._get_secret("lb_stats_test")
            self.db_name = "impact"
            self.db_user = secrets["username"]
            self.db_password = secrets["password"]
            self.db_host = secrets["host"]
            self.db_port = secrets["port"]
            self.sentry_dsn = secrets["sbc_sentry_dsn"]

            self.user_pool_id = secrets["aws_user_pool_id"]
            self.user_pool_client_id = secrets["aws_user_pool_client_id"]

            # Load OpenAI secrets
            secret_string = client.get_secret_value(SecretId="openai")["SecretString"]
            secrets = json.loads(secret_string)
            self.open_ai_key = secrets["Authorization"]

            # Load Twilio secrets
            secret_string = client.get_secret_value(SecretId="twilio")["SecretString"]
            secrets = json.loads(secret_string)
            self.twilio_account_sid = secrets["account_sid"]
            self.twilio_auth_token = secrets["auth_token"]
            self.twilio_whatapp_number = secrets["from_whatsapp"]
            self.twilio_sms_number = secrets["from_sms"]

        except Exception as err:
            raise err

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
