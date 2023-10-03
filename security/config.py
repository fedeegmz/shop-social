from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app_name: str = "Shop Social"
    # admin_email: str = "example@email.com"
    is_test_db: bool
    jwt_secretkey: str
    mongodb_user: str
    mongodb_password: str
    mongodb_host: str
    redis_limiter_host: str
    redis_limiter_port: str
    redis_limiter_password: str
    password_for_testing: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
