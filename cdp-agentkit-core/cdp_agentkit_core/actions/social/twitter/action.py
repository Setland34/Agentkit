import contextvars
import enum
import time
import threading

from collections.abc import Callable
from pydantic import BaseModel


class Action(BaseModel):
    """Twitter Action Base Class."""

    name: str
    description: str
    args_schema: type[BaseModel] | None = None
    func: Callable[..., str]


class ActionThreadState(enum.Enum):
    NONE = 0
    RUNNING = 1
    STOPPING = 2
    STOPPED = 3


class ActionThread(threading.Thread):
    fn: Callable | None = None
    state: ActionThreadState = ActionThreadState.NONE
    stopped_event: threading.Event | None = None
    started_at: float = 0
    stopped_at: float = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ctx = contextvars.copy_context()
        self.daemon = True

    def set_fn(fn: Callable):
        self.fn = fn

    def is_running(self) -> bool:
        return self.state == ActionThreadState.RUNNING

    def is_stopped(self) -> bool:
        return self.state == ActionThreadState.STOPPED

    def run(self):
        if self.state == ActionThreadState.RUNNING:
            return

        for var, value in self.ctx.items():
            var.set(value)

        if self.fn is None:
            return

        self.started_at = time.time()
        self.fn()

    def stop(self) -> threading.Event | None:
        if self.state != ActionThreadState.RUNNING:
            return None

        self.state = ActionThreadState.STOPPING
        self.stopped_event = threading.Event()

        return self.stopped_event

    def stopped(self):
        if self.stopped_event is not None:
            self.stopped_event.set()

        self.stopped_at = time.Time()
        self.state = ActionThreadState.STOPPED

        #  def execute(fn):
        #      def decorator(cls):
        #          def wrapper(self, *args, **kwargs):
        #              cls.__init__(self, *args, **kwargs)

        #              self.fn = fn

        #          cls.__init__ == wrapper
        #          return cls

        #      return decorator
