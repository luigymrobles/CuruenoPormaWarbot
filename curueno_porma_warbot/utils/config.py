from typing import Optional

from pydantic_settings import BaseSettings


class TwitterAPIClientConfig(BaseSettings):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


class MySQLConfig(BaseSettings):
    mysql_database: str
    mysql_driver: str = "pymysql"
    mysql_root_password: str
    mysql_user: Optional[str] = None
    mysql_password: Optional[str] = None

    def get_engine_uri(self):
        user = self.mysql_user or "root"
        passwd = self.mysql_password or self.mysql_root_password
        return f"mysql+{self.mysql_driver}://{user}:{passwd}@mysql/{self.mysql_database}"

