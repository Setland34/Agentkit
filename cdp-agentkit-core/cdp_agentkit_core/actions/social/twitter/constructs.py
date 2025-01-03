from multiprocessing import Manager
from multiprocessing.managers import DictProxy, ListProxy


class Account():
    data: DictProxy | None = None

    def get(self) -> DictProxy:
        if self.data is None:
            self.data = Manager().dict()

        return self.data

    def get_id(self) -> str:
        id = self.get()['id']
        if id is None:
            return ""

        return id

    def get_name(self) -> str:
        name = self.get()['name']
        if name is None:
            return ""

        return name

    def get_username(self) -> str:
        username = self.get()['username']
        if username is None:
            return ""

        return username

    def profile_link(self) -> str:
        return f"https://x.com/{self.get_username()}"

    def load(self, source: dict):
        target = self.get()

        for key, value in source.items():
            if isinstance(value, dict):
                target[key] = self.load(value)
            else:
                target[key] = value


class Mentions():
    collection: ListProxy = None

    def get(self) -> ListProxy:
        if self.collection is None:
            self.collection = Manager().list()

        return self.collection
