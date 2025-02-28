firefly.py
---
Indev

```python
from firefly import Firefly

game = Firefly.find(class_name="UnityWndClass", process_name="StarRail.exe")
# class_name, title, process_name or process_id at least one
match = game.wait("talk.png")
print(match)
# MatchResult(position=Position(left=47, top=840, right=1569, bottom=99), confidence=0.9961451888084412)
game.click(match.position)
```