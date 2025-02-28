# firefly.py

![GitHub License](https://img.shields.io/github/license/GuangChen2333/firefly.py?style=flat-square)
![GitHub Repo stars](https://img.shields.io/github/stars/GuangChen2333/firefly.py?style=flat-square)
![PyPi](https://img.shields.io/pypi/v/firefly.py?style=flat-square)
![Downloads](https://img.shields.io/pypi/dm/firefly.py?style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/firefly.py?style=flat-square)

基于图像识别的窗口自动化库。

## 安装

- **pypi**

```shell
pip install firefly.py
```

## 使用

```python
import PIL.Image
from firefly import Firefly

# 在开始操作前，你需要绑定到一个窗口上
# Firefly.find 方法需要你至少提供class_name, title, process_name, process_id 的其中一个
# 下文将以绑定到星穹铁道窗口为例
game = Firefly.find(class_name="UnityWndClass", process_name="StarRail.exe")
# 现在来看看是否正确吧
print(f"{hex(game.hwnd)} -> {game.title} {game.get_rect()}")
# 0x6c0a52 -> 崩坏：星穹铁道 Rect(left=152, top=70, width=1616, height=939)

# 或者你也可以使用窗口句柄直接绑定
# game = Firefly(0x6c0a52)

# firefly.py 实现了很多必要的方法以供你实现你的自动化
# 下面将实现等待 talk.png 出现并点击它

matched = game.wait(template=PIL.Image.open("./talk.png"), threshold=0.9)
print(matched)
# MatchResult(rect=Rect(left=25, top=814, width=45, height=52), confidence=0.9912481904029846)

# 获取完成, 现在来点击吧
game.right_click(matched.rect.center())

# 需要注意的是, 除非你使用 Position.to_abs_position(game.get_rect()) 与 game.get_rect() 外
# 获取到与传入的都是相对于窗口的坐标
```

### 一些实用方法

```python
import PIL.Image
from firefly import Firefly, MouseButtons, Position

game = Firefly.find(class_name="UnityWndClass", process_name="StarRail.exe")

# 匹配模板
matched = game.match(PIL.Image.open("./talk.png"))
# 等待出现
game.wait(template=game.match(PIL.Image.open("./talk.png")), threshold=0.9, interval=0.5)
# 是否存在
game.exist(game.match(PIL.Image.open("./talk.png")), threshold=0.9)
# 鼠标点击
game.click(
    matched.rect.center(),  # Rect 的中心点
    MouseButtons.LEFT,  # 左键
    times=1,  # 一次
    interval=0,  # 多次点击间隔
    duration=0  # 点击时间
)
# 自定义相对坐标 left, top, right, bottom
pos = Position(0, 0, 0, 0)
# 只用x, y
pos_x_y = Position.from_xy(0, 0, game.get_rect())
# 语法糖
game.left_click(pos_x_y)
# 截图
frame = game.screenshot()
frame.show("这是截图")
```

## 文档

### Class Firefly

Windows 窗口自动化操作工具类

#### 属性: Firefly.hwnd -> int

**窗口句柄**

***

#### 属性: Firefly.title -> str

**窗口标题**

***

#### 属性: Firefly.class_name -> str

**窗口类名**

***

#### 属性: Firefly.pid -> int

**进程ID**

***

#### 属性: Firefly.process_name -> str

**进程名称**

***

#### Firefly.find(class_name: Optional[str] = None, title: Optional[str] = None, process_name: Optional[str] = None, process_id: Optional[int] = None) -> Firefly

**类方法，根据条件查找窗口**

class_name: Optional[str] 窗口类名

title: Optional[str] 窗口标题

process_name: Optional[str] 进程名称

process_id: Optional[int] 进程ID

返回值: Firefly 实例

***

#### Firefly.get_rect() -> Rect

**获取窗口的位置和尺寸（自动处理DPI缩放）**

返回值: Rect 窗口的矩形区域

***

#### Firefly.screenshot() -> PIL.Image.Image

**截取窗口的屏幕截图**

返回值: PIL.Image.Image 截图图像

***

#### Firefly.show() -> None

**显示并激活窗口**

***

#### Firefly.match(template: PIL.Image.Image) -> MatchResult

**模板匹配（使用OpenCV的模板匹配算法）**

template: PIL.Image.Image 模板图片

返回值: MatchResult 匹配结果（包含坐标和置信度）

***

#### Firefly.exist(template: PIL.Image.Image, threshold: float) -> bool

**检查窗口中是否存在模板**

template: PIL.Image.Image 模板图片

threshold: float 置信度阈值

返回值: bool 是否存在匹配

***

#### Firefly.wait(template: PIL.Image.Image, threshold: float, interval: Optional[float] = 0.5) -> MatchResult

**等待直到模板匹配成功**

template: PIL.Image.Image 模板图片

threshold: float 置信度阈值

interval: Optional[float] 检查间隔时间（默认0.5秒）

返回值: MatchResult 匹配结果

***

#### Firefly.click(rel_position: Position, button: MouseButtons = MouseButtons.LEFT, times: Optional[int] = 1, interval: Optional[float] = 0.0, duration: Optional[float] = 0.0) -> None

**在相对位置执行鼠标点击**

rel_position: Position 相对于窗口的位置

button: MouseButtons 鼠标按钮（默认左键）

times: Optional[int] 点击次数（默认1次）

interval: Optional[float] 点击间隔时间（默认0.0秒）

duration: Optional[float] 移动持续时间（默认0.0秒）

***

#### Firefly.left_click(rel_position: Position) -> None

**左键单击**

rel_position: Position 相对于窗口的位置

***

#### Firefly.double_click(rel_position: Position) -> None

**左键双击**

rel_position: Position 相对于窗口的位置

***

#### Firefly.right_click(rel_position: Position) -> None

**右键单击**

rel_position: Position 相对于窗口的位置

***

#### Firefly.middle_click(rel_position: Position) -> None

**中键单击**

rel_position: Position 相对于窗口的位置

***

#### Firefly.move_to(rel_position: Position, duration: Optional[float] = 0.0)

**移动鼠标到指定位置**

rel_position: Position 相对于窗口的位置

duration: Optional[float] 移动持续时间（默认0.0秒）

***

#### Firefly.drag_to(rel_position: Position, button: MouseButtons = MouseButtons.LEFT, duration: Optional[float] = 0.0)

**拖拽到指定位置**

rel_position: Position 相对于窗口的位置

button: MouseButtons 鼠标按钮（默认左键）

duration: Optional[float] 拖拽持续时间（默认0.0秒）

***

#### Firefly.move_rel(x_offset: int, y_offset: int, duration: Optional[float] = 0.0)

**静态方法，相对移动鼠标**

x_offset: int X轴偏移量

y_offset: int Y轴偏移量

duration: Optional[float] 移动持续时间（默认0.0秒）

***

#### Firefly.drag_rel(x_offset: int, y_offset: int, button: MouseButtons = MouseButtons.LEFT, duration: Optional[float] = 0.0)

**静态方法，相对拖拽鼠标**

x_offset: int X轴偏移量

y_offset: int Y轴偏移量

button: MouseButtons 鼠标按钮（默认左键）

duration: Optional[float] 拖拽持续时间（默认0.0秒）

***

#### Firefly.scroll(clicks: float)

**静态方法，滚动鼠标滚轮**

clicks: float 滚动量（正数向上，负数向下）

***

#### Firefly.write(msg: str, interval: Optional[float] = 0.0)

**静态方法，模拟键盘输入**

msg: str 要输入的文本

interval: Optional[float] 输入间隔时间（默认0.0秒）

***

#### Firefly.hot_key(*keys)

**静态方法，组合键操作**

*keys: 要按下的多个按键（如："ctrl", "c"）

***

#### Firefly.get_mouse_position()

**获取鼠标在窗口坐标系中的位置**

返回值: Position 鼠标相对窗口的位置