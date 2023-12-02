from pydantic_settings import BaseSettings


class TwitterAPIClientConfig(BaseSettings):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
