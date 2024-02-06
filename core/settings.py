from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    database_url: str
    tg_id: str
    token: str
    sender: str
    password_email: str
    smtp_server: str
    port: int
    db_host: str = 'db'
    db_port: int
    # postgres_user: str = 'postgress'
    # postgres_password: str = 'postgress'

    class Config:
        env_file = '.env'


settings = Settings()
