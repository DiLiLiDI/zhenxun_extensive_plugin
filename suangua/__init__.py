import random
import json as json
from pathlib import Path
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.params import CommandArg, Arg
from utils.message_builder import image
from nonebot_plugin_apscheduler import scheduler

__zx_plugin_name__ = "算卦"
__plugin_usage__ = """
usage：
	算卦不算命
	指令：
		算卦
""".strip()
__plugin_version__ = "1.0"
__plugin_des__ = "每日一卦"
__plugin_author__ = "DiLiDiLi"
__plugin_type__ = ("群内小游戏",)
__plugin_cmd__ = ["算卦/来一卦"]
__plugin_settings__ = {
	"level": 5,
	"default_status": True,
	"limit_superuser": False,
	"cmd": ["算卦"],
}

suangua_record = Path(__file__).parent / 'suangua.json'
GUAXIANG_PATH = Path(__file__).parent / '64.json'
GUA_IMAGE_PATH = Path(__file__).parent / 'gua'


# 定义读写json文件的函数
def read_json_file(file: Path, info=None) -> dict:
	with file.open("r", encoding="utf-8") as f:
		content = f.read()
		if info is not None:
			with file.open("w", encoding="utf-8") as f:
				f.write(json.dumps(info, indent=4, ensure_ascii=False))
			return {"data": json.loads(content)}
		else:
			return json.loads(content)


# 创建命令处理对象
suangua = on_command("算卦", aliases={"来一卦"}, priority=5, block=True)


# 定义命令处理函数
@suangua.handle()
async def handle_suangua(bot: Bot, event: Event,  arg: Message = CommandArg()):
	if not suangua_record.exists():
		with open(suangua_record, "w", encoding="utf-8") as f:
			f.write('{}')
	guaxiang_info = read_json_file(Path(GUAXIANG_PATH))
	record = read_json_file(suangua_record)
	gid, uid = str(event.group_id), str(event.user_id)

	try:
		if record[gid]:
			try:
				if record[gid][uid]:
					result = record[gid][uid]
					msg_text = guaxiang_info[result]
					msg_image = image(f"{GUA_IMAGE_PATH}/{result}.jpg")
					await suangua.finish("不能再窥探天机了！\n" + "上一次的卦象是：\n" + msg_image + msg_text, at_sender=True)
			except KeyError:
				result = random.randint(1, 64)
				msg_text = guaxiang_info[result]
				msg_image = image(f"{GUA_IMAGE_PATH}/{result}.jpg")
				read_json_file(suangua_record, result)
				await suangua.finish(msg_image + msg_text, at_sender=True)
	except KeyError:
		record[gid] = {}
		result = random.randint(1, 64)
		msg_text = guaxiang_info[result]
		msg_image = image(f"{GUA_IMAGE_PATH}/{result}.jpg")
		record[gid][uid] = result
		read_json_file(suangua_record, record)
		await suangua.finish(msg_image + msg_text, at_sender=True)


@scheduler.scheduled_job("cron", hour=0, minute=0, misfire_grace_time=60)
async def clear_suangua_data():
	if suangua_record.exists():
		suangua_record.unlink()
