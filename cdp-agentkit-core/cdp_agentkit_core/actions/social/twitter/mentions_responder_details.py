from collections.abc import Callable

from pydantic import BaseModel

from cdp_agentkit_core.actions.social.twitter import TwitterAction, TwitterContext

MENTIONS_RESPONDER_DETAILS_PROMPT = """
"""

class MentionsResponderDetailsInput(BaseModel):
    pass

def mentions_responder_details(context: TwitterContext) -> str:
    pass

class MentionsResponderDetailsAction(TwitterAction):
    name: str = "mentions_responder_details"
    description: str = MENTIONS_RESPONDER_DETAILS_PROMPT
    args_schema: type[BaseModel] | None = MentionsResponderDetailsInput
    func: Callable[..., str] = mentions_responder_details
