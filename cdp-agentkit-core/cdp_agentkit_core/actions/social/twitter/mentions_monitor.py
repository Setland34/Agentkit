from queue import Queue
from time import sleep

import tweepy
from pydantic import BaseModel

from cdp_agentkit_core.actions.social.twitter import (
    TwitterActionThread,
    TwitterActionThreadState,
)

from cdp_agentkit_core.actions.social.twitter.context import context


class MentionsMonitor(TwitterActionThread):
    CONTEXT_KEY: str = "mentions-monitor"

    """
    https://developer.x.com/en/docs/x-api/rate-limits
    """
    backoff: list[int] = [2, 60, 15*60]

    """
    current position within the backoff list
    """
    backoff_index: int = 0

    ""
    errors: Queue = Queue()
    ""

    """
    ammount of time waited since the last successful call.
    """
    waited: int = 0

    """
    last mention id retrieved
    """
    mention_id: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fn = self.monitor

    def monitor(self):
        ctx = context()
        client = ctx.client.get()

        if client is None:
            raise RuntimeError("Twitter (X) client is unavailable.")

        #  self.state = TwitterActionThreadState.RUNNING
        #  while self.state == TwitterActionThreadState.RUNNING:
        #      sleep(1)

        #  self.stopped()
        #  return

        try:
            response = client.get_me()
            me = response.data
        except tweepy.errors.TweepyException as e:
            raise e

        self.state = TwitterActionThreadState.RUNNING
        while self.state == TwitterActionThreadState.RUNNING:
            self.waited += 1

            if self.waited < self.backoff[self.backoff_index]:
                sleep(1)
                continue

            try:
                response = client.get_users_mentions(me.id, since_id=self.mention_id)
                mentions = response.data
            except tweepy.errors.TweepyException as e:
                self.errors.put(e)
                self.backoff_index = min(self.backoff_index + 1, len(self.backoff) - 1)

                if self.backoff[self.backoff_index] > self.waited:
                    self.waited = 0

                continue

            self.process(mentions)
            self.waited = 0

        self.stopped()

    def process(self, mentions):
        ctx = context()
        collection = ctx.mentions.get()

        for mention in mentions:
            if mention is None:
                continue

            collection.append(mention)

        self.mention_id = mention.id
