import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://api.qqsuu.cn/api/" #https://api.qqsuu.cn/

@plugins.register(name="moyu",
                  desc="获取摸鱼日历",
                  version="1.0",
                  author="masterke",
                  desire_priority=100)
class moyu(Plugin):
    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【摸鱼】获取摸鱼日历"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()
        if self.content == "摸鱼":
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.moyu()
            if result != None:
                reply.type = ReplyType.IMAGE_URL if type(result) == str else ReplyType.IMAGE
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS

    def moyu(self):
        url = BASE_URL_DM + "dm-moyu"
        parameter = "type=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            response = requests.get(url, params=parameter,headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('code') == 200 and json_data['data']:
                    img_url = json_data['data']
                    logger.info(json_data)
                    return img_url
                else:
                    logger.info(json_data)
            else:
                logger.info(f"接口异常：{response.status_code}")
        except Exception as e:
            logger.error(f"接口异常：{e}")
                
        logger.error("所有接口都挂了,无法获取")
        return None
