from cdp_agentkit_core.actions.social.twitter.action import (
    Action as TwitterAction,
    ActionThread as TwitterActionThread,
    ActionThreadState as TwitterActionThreadState,
)
from cdp_agentkit_core.actions.social.twitter.constructs import (
    Account as TwitterAccount,
    Mentions as TwitterMentions,
)
from cdp_agentkit_core.actions.social.twitter.context import TwitterContext as TwitterContext

from cdp_agentkit_core.actions.social.twitter.account_details import AccountDetailsAction
from cdp_agentkit_core.actions.social.twitter.mentions_monitor_details import (
    MentionsMonitorDetailsAction as TwitterMentionsMonitorDetailsAction,
)
from cdp_agentkit_core.actions.social.twitter.mentions_monitor import (
    MentionsMonitor as TwitterMentionsMonitor,
)
from cdp_agentkit_core.actions.social.twitter.mentions_monitor_start import (
    MentionsMonitorStartAction as TwitterMentionsMonitorStartAction,
)
from cdp_agentkit_core.actions.social.twitter.mentions_monitor_stop import (
    MentionsMonitorStopAction as TwitterMentionsMonitorStoptAction
)
from cdp_agentkit_core.actions.social.twitter.mentions_responder_details import (
    MentionsResponderDetailsAction as TwitterMentionsResponderDetailsAction,
)
from cdp_agentkit_core.actions.social.twitter.mentions_responder_start import (
    MentionsResponderStartAction as TwitterMentionsResponderStartAction,
)
from cdp_agentkit_core.actions.social.twitter.mentions_responder_stop import (
    MentionsResponderStopAction as TwitterMentionsResponderStopAction,
)
from cdp_agentkit_core.actions.social.twitter.post_tweet import (
    PostTweetAction as TwitterPostTweetAction
)


def get_all_twitter_actions() -> list[type[TwitterAction]]:
    actions = []
    for action in TwitterAction.__subclasses__():
        actions.append(action())

    return actions


TWITTER_ACTIONS = get_all_twitter_actions()

__all__ = [
    "TwitterAction",
    "TwitterActionThread",
    "TwitterContext",

    "TwitterAccountDetailsAction",
    "TwitterMentionsMonitorDetailsAction",
    "TwitterMentionsMonitorStartAction",
    "TwitterMentionsMonitorStopAction",
    "TwitterMentionsResponderDetailsAction",
    "TwitterMentionsResponderStartAction",
    "TwitterMentionsResponderStopAction",
    "TwitterPostTweetAction",

    "TWITTER_ACTIONS",
]
