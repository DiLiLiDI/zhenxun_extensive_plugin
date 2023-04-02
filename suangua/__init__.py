import random
import json as json
from pathlib import Path
from services.log import logger
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

dir_path = Path(__file__).parent
gua_path = dir_path / 'gua'
suangua_record = dir_path / 'suangua.json'


def readInfo(file, info=None):
	path = Path(file)
	with path.open("r", encoding="utf-8") as f:
		context = f.read()
		if info is not None:
			with path.open("w", encoding="utf-8") as f:
				f.write(json.dumps(info, indent=4, ensure_ascii=False))
			with path.open("r", encoding="utf-8") as f:
				data = f.read()
			return {"data": json.loads(context.strip())}
		else:
			return json.loads(context.strip())


# 创建命令对象
suangua = on_command("算卦", aliases={"来一卦"}, priority=5, block=True)


# 定义处理函数
@suangua.handle()
async def handle_suangua(bot: Bot, event: Event, arg: Message = CommandArg()):
	if not suangua_record.exists():
		with open(suangua_record, "w", encoding="utf-8") as f:
			f.write('{}')
	gid: str = str(event.group_id)
	uid: str = str(event.user_id)
	guaxiang = open(f"{dir_path}/64.json", 'r', encoding='utf-8')
	guaxiang_content = guaxiang.read()
	array_json = json.loads(guaxiang_content)
	content = readInfo(suangua_record)
	# 检查用户是否在字典中
	try:
		if content[gid]:
			pass
	except KeyError:
		content[gid] = {}
	try:
		if content[gid][uid]:
			json_file_gua = open(suangua_record)
			json_gua_content = json_file_gua.read()
			last_data = json.loads(json_gua_content)
			result = last_data[gid][uid]
			msg_text = array_json[result]
			logger.info(f"算卦：第{result}卦")
			msg_image = image(f"{gua_path}/{result}.jpg")
			await suangua.finish("不能再窥探天机了！\n" + "上一次的卦象是：\n" + msg_image + msg_text, at_sender=True)
	except KeyError:
		rand = random.randint(0, 64)
		msg_text = array_json[rand]
		logger.info(f"算卦：第{rand}卦")
		msg_image = image(f"{gua_path}/{rand}.jpg")
		content[gid][uid] = rand
		readInfo(suangua_record, content)
		await suangua.finish(msg_image + msg_text, at_sender=True)


@scheduler.scheduled_job("cron", hour=0, minute=0, misfire_grace_time=60)
async def clear_suangua_data():
	if suangua_record.exists():
		suangua_record.unlink()
