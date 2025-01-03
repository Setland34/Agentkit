from collections.abc import Callable

from pydantic import BaseModel

from cdp_agentkit_core.actions.social.twitter import TwitterAction, TwitterContext

MENTIONS_DETAILS_PROMPT = """show mentions for the current Twitter (X) account"""


class MentionsDetailsInput(BaseModel):
    pass


def mentions_details(context: TwitterContext) -> str:
    ctx = context()
    mentions = list(ctx.mentions.get())

    data = {
        "mentions": mentions,
        "mentions-count": len(mentions),
    }

    json = dumps(data)

    return json


class MentionsDetailsAction(TwitterAction):
    name: str = "mentions_details"
    description: str = MENTIONS_DETAILS_PROMPT
    args_schema: type[BaseModel] | None = MentionsDetailsInput
    func: Callable[..., str] = account_details
