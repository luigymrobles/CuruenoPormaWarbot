import tweepy as tw
from typing import Optional

from curueno_porma_warbot.utils.config import TwitterAPIClientConfig
from curueno_porma_warbot.utils.log import ClassWithLogger


class TwitterAPIClient(ClassWithLogger):
	"""Class to Manage Twitter API connection."""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config = TwitterAPIClientConfig()

		self.auth = tw.OAuthHandler(self.config.consumer_key, self.config.consumer_secret)
		self.auth.set_access_token(self.config.access_token, self.config.access_token_secret)
		self.client = tw.Client(**dict(self.config))
		self.api = tw.API(auth=self.auth)

		self.logger.info("Ready!")

	def send_tweet(self, tweet_text: str = "", media_path: Optional[str] = None) -> None:
		"""Sends a Tweet with the tweet_text as content and media_path as attachment
		if any provided.

		:param tweet_text: The string with the Tweet content.
		:param media_path: The string path to the media file to upload.
		"""
		if media_path is None:
			self.client.create_tweet(text=tweet_text)
		else:
			media = self.api.media_upload(filename=media_path)
			self.client.create_tweet(text=tweet_text, media_ids=[media.media_id])
		self.logger.info("Tweet sent!")
