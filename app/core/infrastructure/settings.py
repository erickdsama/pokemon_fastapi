from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    db_port: int = 5432


class GlobalBaseSettings(DatabaseSettings):
    jwt_key = "5hip11n853Cr33$$"
    ...


class DevelopmentSettings(GlobalBaseSettings):
    ...


environment_settings = {
    "production": GlobalBaseSettings(),
    "development": GlobalBaseSettings(),
}
