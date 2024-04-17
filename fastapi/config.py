import sys
from typing import Literal

from pydantic import EmailStr, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = "../.env.dev"
if "pytest" in sys.modules:
    ENV_FILE = "tests/.env.test"


class Settings(BaseSettings):
    domain: str

    mode: Literal["DEV", "TEST", "PROD"]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    relo_host: str
    relo_port: int

    db_scheme: str
    db_async_scheme: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name_relohelper: str
    db_name_security: str

    @computed_field  # type: ignore[misc]
    @property
    def relohelper_url(self) -> str:
        return PostgresDsn.build(
            scheme=self.db_scheme,
            username=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name_relohelper,
        ).unicode_string()

    @computed_field  # type: ignore[misc]
    @property
    def relohelper_async_url(self) -> str:
        return PostgresDsn.build(
            scheme=self.db_async_scheme,
            username=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name_relohelper,
        ).unicode_string()

    @computed_field  # type: ignore[misc]
    @property
    def security_url(self) -> str:
        return PostgresDsn.build(
            scheme=self.db_scheme,
            username=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name_security,
        ).unicode_string()

    # OAuth2
    jwt_secret: str
    algorithm: Literal[
        "HS256", "HS384", "HS512",
        "RS256", "RS384", "RS512",
        "ES256", "ES384", "ES512",
        "PS256", "PS384", "PS512",
    ]  # fmt: skip
    access_token_expire_minutes: int

    # Registration by Email
    smtp_host: str
    smtp_port: int
    email: EmailStr
    email_password: str

    # Profiling with PyInstrument
    profiling: bool
    interval: float
    async_mode: Literal["enabled", "disabled", "strict"]

    # TestUser for PyTest
    test_username: str | None = None
    test_email: EmailStr | None = None
    test_password: str | None = None
    test_role: Literal["user", "admin"] | None = None

    # Observability on Grafana
    app_name: str
    otlp_grpc_endpoint: str
    prometheus_multiproc_dir: str | None = None

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()  # type: ignore[call-arg]
