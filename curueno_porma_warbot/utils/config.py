from pydantic_settings import BaseSettings


class TwitterAPIClientConfig(BaseSettings):
    """Secrets for the Twitter API"""
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


class MySQLConfig(BaseSettings):
    """Secrets for the DB connection"""
    mysql_database: str
    mysql_driver: str = "pymysql"
    mysql_root_password: str
    mysql_user: str | None = None
    mysql_password: str | None = None
    mysql_verbose: bool = False

    def get_engine_uri(self):
        user = self.mysql_user or "root"
        passwd = self.mysql_password or self.mysql_root_password
        return f"mysql+{self.mysql_driver}://{user}:{passwd}@mysql/{self.mysql_database}"

