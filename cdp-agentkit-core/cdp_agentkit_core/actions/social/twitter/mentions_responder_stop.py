from collections.abc import Callable

from pydantic import BaseModel

from cdp_agentkit_core.actions.social.twitter import TwitterAction, TwitterContext

MENTIONS_RESPONDER_STOP_PROMPT = """
"""

class MentionsResponderStopInput(BaseModel):
    pass

def mentions_responder_stop(context: TwitterContext) -> str:
    pass

class MentionsResponderStopAction(TwitterAction):
    name: str = "mentions_responder_stop"
    description: str = MENTIONS_RESPONDER_STOP_PROMPT
    args_schema: type[BaseModel] | None = MentionsResponderStopInput
    func: Callable[..., str] = mentions_responder_stop
