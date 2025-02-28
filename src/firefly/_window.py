from typing import TypeVar, Optional

# noinspection PyPackageRequirements
import win32gui
import win32con
import win32process
import psutil

from ._enums import FindConditions
from ._exceptions import WindowNotFoundError

T = TypeVar("T", bound="Window")


class Window:
    def __init__(self, hwnd: int):
        self._hwnd = hwnd

        self._class_name = win32gui.GetClassName(self._hwnd)
        self._title = win32gui.GetWindowText(self._hwnd)
        _, self._pid = win32process.GetWindowThreadProcessId(self._hwnd)
        self._process_name = ""

        try:
            process = psutil.Process(self._pid)
            self._process_name = process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    @classmethod
    def find(
            cls,
            class_name: Optional[str] = None,
            title: Optional[str] = None,
            process_name: Optional[str] = None
    ) -> T:
        required_conditions = []
        if class_name is not None:
            required_conditions.append((FindConditions.CLASS_NAME, class_name))
        if title is not None:
            required_conditions.append((FindConditions.TITLE, title))
        if process_name is not None:
            required_conditions.append((FindConditions.PROCESS_NAME, process_name))

        num_conditions = len(required_conditions)

        if num_conditions == 0:
            raise TypeError("At least one search condition required (class_name, title or process_name)")

        max_confidence = 0.0
        best_hwnd = 0

        def enum_callback(hwnd: int, _):
            nonlocal max_confidence, best_hwnd
            current_matches = 0

            for condition_type, expected in required_conditions:
                actual = None

                match condition_type:
                    case FindConditions.CLASS_NAME:
                        actual = win32gui.GetClassName(hwnd)
                    case FindConditions.TITLE:
                        actual = win32gui.GetWindowText(hwnd)
                    case FindConditions.PROCESS_NAME:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        if pid is not None:
                            try:
                                process = psutil.Process(pid)
                                actual = process.name()
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass

                if actual == expected:
                    current_matches += 1
                else:
                    break

            if current_matches > 0:
                confidence = current_matches / num_conditions
                if confidence > max_confidence:
                    max_confidence = confidence
                    best_hwnd = hwnd

            return True

        win32gui.EnumWindows(enum_callback, None)

        if best_hwnd == 0:
            raise WindowNotFoundError("Cannot find the window by conditions.")

        return cls(best_hwnd)

    @property
    def hwnd(self) -> int:
        return self._hwnd

    @property
    def title(self) -> str:
        return self._title

    @property
    def class_name(self) -> str:
        return self._class_name

    @property
    def pid(self) -> str:
        return self._pid

    @property
    def process_name(self) -> str:
        return self._process_name

    def show(self) -> None:
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)
