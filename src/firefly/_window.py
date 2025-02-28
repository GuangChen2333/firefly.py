import ctypes
import time

from typing import Optional

import PIL.Image
import pyautogui
# noinspection PyPackageRequirements
import win32gui
import win32con
import win32process
import psutil
import cv2
import numpy

from ._enums import FindConditions, MouseButtons
from ._exceptions import WindowNotFoundError
from ._structures import Position, Rect, MatchResult


class Firefly:
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
            process_name: Optional[str] = None,
            process_id: Optional[int] = None
    ):
        required_conditions = []
        if class_name is not None:
            required_conditions.append((FindConditions.CLASS_NAME, class_name))
        if title is not None:
            required_conditions.append((FindConditions.TITLE, title))
        if process_name is not None:
            required_conditions.append((FindConditions.PROCESS_NAME, process_name))
        if process_id is not None:
            required_conditions.append((FindConditions.PROCESS_ID, process_id))

        num_conditions = len(required_conditions)

        if num_conditions == 0:
            raise TypeError("At least one search condition required (class_name, title, process_name or process_id)")

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
                    case FindConditions.PROCESS_ID:
                        _, actual = win32process.GetWindowThreadProcessId(hwnd)

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
    def pid(self) -> int:
        return self._pid

    @property
    def process_name(self) -> str:
        return self._process_name

    def get_rect(self) -> Rect:
        rect = Position(*(win32gui.GetWindowRect(self.hwnd)))

        user32 = ctypes.WinDLL('user32')
        dpi = user32.GetDpiForSystem()

        scaling_factor = dpi / 96.0
        return Rect(
            int(rect.left * scaling_factor),
            int(rect.top * scaling_factor),
            int((rect.right - rect.left) * scaling_factor),
            int((rect.bottom - rect.top) * scaling_factor)
        )

    def screenshot(self) -> PIL.Image.Image:
        return pyautogui.screenshot(region=self.get_rect().to_region())

    def show(self) -> None:
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwnd)

    def match(self, template: PIL.Image.Image) -> MatchResult:
        screenshot = cv2.cvtColor(numpy.array(self.screenshot()), cv2.COLOR_RGB2BGR)
        template = cv2.cvtColor(numpy.array(template), cv2.COLOR_RGB2BGR)
        height, width = template.shape[:2]

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        return MatchResult(Rect(max_loc[0], max_loc[1], width, height), max_val)

    def exist(self, template: PIL.Image.Image, threshold: float) -> bool:
        result = self.match(template)
        return result.confidence >= threshold

    def wait(self, template: PIL.Image.Image, threshold: float, interval: Optional[float] = 0.5) -> MatchResult:
        while True:
            result = self.match(template)
            if result.confidence >= threshold:
                return result
            time.sleep(interval)

    def click(
            self,
            rel_position: Position,
            button: MouseButtons = MouseButtons.LEFT,
            times: Optional[int] = 1,
            interval: Optional[float] = 0.0,
            duration: Optional[float] = 0.0,
    ) -> None:
        abs_position = rel_position.to_abs_position(self.get_rect())
        # noinspection PyTypeChecker
        pyautogui.click(
            *abs_position.to_xy(),
            button=button.value,
            clicks=times,
            interval=interval,
            duration=duration
        )

    def left_click(self, rel_position: Position) -> None:
        self.click(rel_position, button=MouseButtons.LEFT)

    def double_click(self, rel_position: Position) -> None:
        self.click(rel_position, button=MouseButtons.LEFT, times=2)

    def right_click(self, rel_position: Position) -> None:
        self.click(rel_position, button=MouseButtons.RIGHT)

    def middle_click(self, rel_position: Position) -> None:
        self.click(rel_position, button=MouseButtons.MIDDLE)

    def move_to(self, rel_position: Position, duration: Optional[float] = 0.0):
        pyautogui.moveTo(*rel_position.to_abs_position(self.get_rect()).to_xy(), duration=duration)

    def drag_to(
            self,
            rel_position: Position,
            button: MouseButtons = MouseButtons.LEFT,
            duration: Optional[float] = 0.0
    ):
        # noinspection PyTypeChecker
        pyautogui.dragTo(*rel_position.to_abs_position(self.get_rect()).to_xy(), duration=duration, button=button.value)

    @staticmethod
    def move_rel(x_offset: int, y_offset: int, duration: Optional[float] = 0.0):
        pyautogui.moveRel(x_offset, y_offset, duration=duration)

    @staticmethod
    def drag_rel(
            x_offset: int,
            y_offset: int,
            button: MouseButtons = MouseButtons.LEFT,
            duration: Optional[float] = 0.0
    ):
        # noinspection PyTypeChecker
        pyautogui.dragRel(x_offset, y_offset, duration=duration, button=button.value)

    @staticmethod
    def scroll(clicks: float):
        pyautogui.scroll(clicks)

    @staticmethod
    def mouse_down(x: int, y: int, button: MouseButtons = MouseButtons.LEFT):
        # noinspection PyTypeChecker
        pyautogui.mouseDown(x, y, button=button.value)

    @staticmethod
    def mouse_up(x: int, y: int, button: MouseButtons = MouseButtons.LEFT):
        # noinspection PyTypeChecker
        pyautogui.mouseUp(x, y, button=button.value)

    @staticmethod
    def write(msg: str, interval: Optional[float] = 0.0):
        pyautogui.write(msg, interval=interval)

    @staticmethod
    def press(keys: list[str], interval: Optional[float] = 0.0):
        pyautogui.press(keys, interval=interval)

    @staticmethod
    def key_down(key: str):
        pyautogui.keyDown(key)

    @staticmethod
    def key_up(key: str):
        pyautogui.keyUp(key)

    @staticmethod
    def hot_key(*keys):
        pyautogui.hotkey(*keys)

    def get_mouse_position(self):
        pos = pyautogui.position()
        return Position.from_xy(int(pos.x), int(pos.y), self.get_rect())
