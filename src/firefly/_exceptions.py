from typing import Optional


class WindowNotFoundError(Exception):
    def __init__(self, msg: Optional[str] = ""):
        self._msg = msg
        super().__init__(msg)

    @property
    def msg(self):
        return self._msg


class WindowOperationError(Exception):
    def __init__(self, hwnd: int, msg: Optional[str] = ""):
        self._hwnd = hwnd
        self._msg = msg
        super().__init__(f"[{hwnd}] {msg}")

    @property
    def hwnd(self):
        return self._hwnd

    @property
    def msg(self):
        return self._msg
