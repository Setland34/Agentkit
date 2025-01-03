from collections.abc import Callable
from json import dumps

from pydantic import BaseModel

from cdp_agentkit_core.actions.social.twitter import (
    TwitterAction,
)
from cdp_agentkit_core.actions.social.twitter.context import context
from cdp_agentkit_core.actions.social.twitter.mentions_monitor import MentionsMonitor

MENTIONS_MONITOR_DETAILS_PROMPT = """show details for the mention monitor."""


class MentionsMonitorDetailsInput(BaseModel):
    pass


def mentions_monitor_details() -> str:
    ctx = context()
    monitor = ctx.get(MentionsMonitor.CONTEXT_KEY)

    if monitor is None:
        return "monitor has not been started."

    mentions = list(ctx.mentions.get())

    data = {
        "is-monitor-running": monitor.is_running(),
        "mentions": mentions,
        "mentions-count": len(mentions),
    }

    json = dumps(data)

    return f"""
        please find the status of the monitor in json format below:
        {json}
    """


class MentionsMonitorDetailsAction(TwitterAction):
    name: str = "mentions_monitor_details"
    description: str = MENTIONS_MONITOR_DETAILS_PROMPT
    args_schema: type[BaseModel] | None = MentionsMonitorDetailsInput
    func: Callable[..., str] = mentions_monitor_details
