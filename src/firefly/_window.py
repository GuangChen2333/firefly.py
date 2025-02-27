from typing import TypeVar, Optional

# noinspection PyPackageRequirements
import win32gui
import win32con
import psutil
import win32process

from ._exceptions import WindowNotFoundError, WindowOperationError

T = TypeVar("T", bound="Window")


class Window:
    def __init__(self, hwnd: int):
        self._hwnd = hwnd

    @classmethod
    def find(cls, class_name: Optional[str] = None, title: Optional[str] = None, process_name: Optional[str] = None):
        windows = []

        def enum_callback(w_hwnd: int, _) -> bool:
            nonlocal windows

            w_class_name = win32gui.GetClassName(w_hwnd)
            w_windows_title = win32gui.GetWindowText(w_hwnd)
            _, w_pid = win32process.GetWindowThreadProcessId(w_hwnd)
            w_process_name = None

            if w_pid:
                try:
                    w_process = psutil.Process(w_pid)
                    w_process_name = w_process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            windows.append(
                (
                    w_hwnd,
                    w_class_name,
                    w_windows_title,
                    w_process_name
                )
            )

            return True

        conditions = [class_name, title, process_name]
        num_conditions = sum(1 for condition in conditions if condition is not None)

        if num_conditions == 0:
            raise TypeError("At least one search condition required (class_name, title or process_name)")

        win32gui.EnumWindows(enum_callback, None)

        max_confidence = 0.0
        best_hwnd = None

        for t_hwnd, t_class_name, t_title, t_process_name in windows:
            score = 0

            if t_class_name and t_class_name == class_name:
                score += 1
            if t_title and t_title == title:
                score += 1
            if t_process_name and t_process_name == process_name:
                score += 1

            confidence = score / num_conditions
            if confidence > max_confidence:
                max_confidence = confidence
                best_hwnd = t_hwnd

        if best_hwnd is None:
            raise WindowNotFoundError("Cannot find the window by conditions.")

        return cls(best_hwnd)

    @property
    def hwnd(self):
        return self._hwnd

    def show(self) -> None:
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)
