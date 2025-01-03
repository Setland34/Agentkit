from contextvars import ContextVar

from typing import Any, Callable, Generic, Optional, TypeVar
from pydantic import BaseModel, Field, GetCoreSchemaHandler, ConfigDict
from pydantic.fields import FieldInfo
from pydantic_core import CoreSchema, core_schema


class Context():
    class Config:
        arbitrary_types_allowed = True

    cvars: ContextVar[dict] = ContextVar('context_store', default={})

    def __init__(self):
        super(Context, self).__init__()

        if not self.cvars.get():
            self.cvars.set({})

        self._tokens: dict[str, Any] = {}

    def create_var(self, name: str, default=None) -> None:
        store = self.cvars.get()

        if name not in store:
            store[name] = ContextVar(name, default=default)
            self.cvars.set(store)

    def get(self, name: str) -> Optional[Any]:
        store = self.cvars.get()

        if name not in store:
            raise KeyError(f"Context variable '{name}' not found")

        return store[name].get()

    def set(self, name: str, value: Any) -> None:
        store = self.cvars.get()

        if name not in store:
            self.create_var(name)
            store = self.cvars.get()

        self._tokens[name] = store[name].set(value)

    def reset(self, name: str = None) -> None:
        if name is not None:
            if name in self._tokens:
                self._tokens[name].reset()
                del self._tokens[name]

        else:
            for token in self._tokens.values():
                token.reset()

            self._tokens.clear()
            self.cvars.set({})
