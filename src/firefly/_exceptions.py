from typing import Optional


class WindowNotFoundError(Exception):
    def __init__(self, msg: Optional[str] = ""):
        self._msg = msg
        super().__init__(msg)

    @property
    def msg(self):
        return self._msg
