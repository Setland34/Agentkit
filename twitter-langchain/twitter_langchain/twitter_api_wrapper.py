"""Util that calls Twitter API."""

import cdp_agentkit_core.actions.social.twitter.context as context
from pydantic import BaseModel, Field, model_validator
import tweepy
from pydantic import BaseModel, model_validator
import contextvars
from collections.abc import Callable
from typing import Any

from langchain_core.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
import tweepy

from cdp_agentkit_core.actions.social.twitter.context import context


class TwitterApiWrapper(BaseModel):
    """Wrapper for Twitter API."""

    ctx: Any = Field(..., description="context")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ctx = contextvars.copy_context()

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: dict) -> Any:
        """Validate that Twitter access token, token secret, and tweepy exists in the environment."""
        api_key = get_from_dict_or_env(values, "twitter_api_key", "TWITTER_API_KEY")
        api_secret = get_from_dict_or_env(values, "twitter_api_secret", "TWITTER_API_SECRET")
        access_token = get_from_dict_or_env(values, "twitter_access_token", "TWITTER_ACCESS_TOKEN")
        access_token_secret = get_from_dict_or_env(values, "twitter_access_token_secret", "TWITTER_ACCESS_TOKEN_SECRET")
        bearer_token = get_from_dict_or_env(values, "twitter_bearer_token", "TWITTER_BEARER_TOKEN")

        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        ctx = context()
        ctx.client.set(client)

        values["ctx"] = ctx
        values["client"] = client
        values["api_key"] = api_key
        values["api_secret"] = api_secret
        values["access_token"] = access_token
        values["access_token_secret"] = access_token_secret

        return values

    def run_action(self, func: Callable[..., str], **kwargs) -> str:
        """Run a Twitter Action."""

        for var, value in self.ctx.items():
            var.set(value)

        response = func(**kwargs)
        self.ctx = contextvars.copy_context()

        return response
