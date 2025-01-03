from collections.abc import Callable

from pydantic import BaseModel

from cdp_agentkit_core.actions.social.twitter import TwitterAction, TwitterContext

MENTIONS_RESPONDER_START_PROMPT = """
"""

class MentionsResponderStartInput(BaseModel):
    pass

def mentions_responder_start(context: TwitterContext) -> str:
    pass

class MentionsResponderStartAction(TwitterAction):
    name: str = "mentions_responder_start"
    description: str = MENTIONS_RESPONDER_START_PROMPT
    args_schema: type[BaseModel] | None = MentionsResponderStartInput
    func: Callable[..., str] = mentions_responder_start
