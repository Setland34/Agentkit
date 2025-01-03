from collections.abc import Callable

from pydantic import BaseModel

from cdp_agentkit_core.actions.social.twitter import (
    TwitterAction,
)
from cdp_agentkit_core.actions.social.twitter.context import context
from cdp_agentkit_core.actions.social.twitter.mentions_monitor import MentionsMonitor

MENTIONS_MONITOR_STOP_PROMPT = """
Stop monitoring Twitter (X) mentions
"""


class MentionsMonitorStopInput(BaseModel):
    pass


def mentions_monitor_stop() -> str:
    ctx = context()
    monitor = ctx.get(MentionsMonitor.CONTEXT_KEY)
    ctx.set(MentionsMonitor.CONTEXT_KEY, None)

    if monitor is None:
        return "monitor cannot be stopped, it is not running!"

    if monitor.is_running() is False:
        return "monitor has already stopped"

    event = monitor.stop()
    event.wait()

    return "successfully stopped monitoring for Twitter (X) mentions for the authenticated user."


class MentionsMonitorStopAction(TwitterAction):
    name: str = "mentions_monitor_stop"
    description: str = MENTIONS_MONITOR_STOP_PROMPT
    args_schema: type[BaseModel] | None = MentionsMonitorStopInput
    func: Callable[..., str] = mentions_monitor_stop
