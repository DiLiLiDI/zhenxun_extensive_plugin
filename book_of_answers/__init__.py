import random
import json
from pathlib import Path
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

__zx_plugin_name__ = "答案之书"
__plugin_usage__ = """
usage：
    答案之书，通过答案之书寻找你内心问题的答案
    指令:
        [答案之书+你的问题]获取你内心的答案吧
""".strip()
__plugin_version__ = "1.0"
__plugin_des__ = "答案之书，通过答案之书寻找你内心问题的答案"
__plugin_author__ = "DiLiDiLi"
__plugin_type__ = ("群内小游戏",)
__plugin_cmd__ = ["答案之书"]
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["答案之书"],
}

dir_path=Path(__file__).parent
book_of_answers: list[str]
with open(f"{dir_path}/book_of_answers.json", "r", encoding="utf-8") as file:
    book_of_answers = json.load(file)

boa = on_command("答案之书", priority=20, block=True)

@boa.handle()
async def _(bot: Bot, event: MessageEvent):
    await boa.finish(random.choice(book_of_answers), at_sender=True)
