from dotenv import find_dotenv, load_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))

class Database(BaseSettings):
    host: str = Field(default='127.0.0.1', alias='DB_HOST')
    port: int = Field(default=3306, alias='DB_PORT')

    database: str = Field(default="db", alias='DB_DATABASE')
    username: str = Field(default="username", alias='DB_USER')
    password: str = Field(default="password", alias="DB_PASSWORD")

    @computed_field
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}/{self.database}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )
    host: str = Field(default="127.0.0.1", alias="APP_HOST")
    port: int = Field(default=8000, alias="APP_PORT")

    database: Database = Field(default_factory=Database)

    public_base_url: str = Field(alias="PUBLIC_BASE_URL")

    @computed_field
    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

settings = Settings()
