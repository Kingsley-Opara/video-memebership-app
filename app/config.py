from pydantic import BaseSettings, Field
from functools import lru_cache

class Settings(BaseSettings):
    keyspace: str = Field(..., env = 'ASTRADB_KEYSPACE')
    db_client_id: str = Field(..., env='ASTRADB_CLIENT_ID')
    db_client_secret: str = Field(..., env='ASTRADB_CLIENT_SECRET')
    secret_key: str = Field(...)
    jwt_algorithm: str = Field(default='HS256')

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()