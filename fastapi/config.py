from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, EmailStr, PostgresDsn


class Settings(BaseSettings):
    domain: str

    mode: Literal["DEV", "TEST", "PROD"]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name_relohelper: str
    db_name_security: str

    @computed_field
    @property
    def relohelper_url(self) -> PostgresDsn:
        user = f"{self.db_user}:{self.db_pass}"
        database = f"{self.db_host}:{self.db_port}/{self.db_name_relohelper}"
        return f"postgresql://{user}@{database}"

    @computed_field
    @property
    def security_url(self) -> PostgresDsn:
        user = f"{self.db_user}:{self.db_pass}"
        database = f"{self.db_host}:{self.db_port}/{self.db_name_security}"
        return f"postgresql://{user}@{database}"

    # test_db_host: str
    # test_db_port: int
    # test_db_user: str
    # test_db_pass: str
    # test_db_name: str
    #
    # @property
    # def test_database_url(self):
    #     user = f"{self.test_db_user}:{self.test_db_pass}"
    #     database = f"{self.test_db_host}:{self.test_db_port}/{self.test_db_name}"
    #     return f"postgresql+asyncpg://{user}@{database}"

    smtp_host: str
    smtp_port: int
    email: EmailStr
    email_password: str

    # redis_host: str
    # redis_port: int
    #
    # sentry_dsn: str

    # secret_key: str
    # algorithm: str

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")


settings = Settings()
