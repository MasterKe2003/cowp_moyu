import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

@plugins.register(name="moyu",
                  desc="获取摸鱼日历",
                  version="1.1",
                  author="masterke",
                  desire_priority=100)
class moyu(Plugin):
    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")
    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.message = e_context["context"].content.strip()
        if self.message != "摸鱼日历":
            return

        logger.info(f"[{__class__.__name__}] 收到消息: {self.message}")
        result, result_type = self.moyu()
        reply = Reply()
        if result != None:
            reply.type = result_type
            reply.content = result
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        else:
            reply.type = ReplyType.ERROR
            reply.content = "获取失败,等待修复⌛️"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

    def moyu(self):
        url = "https://api.vvhan.com/api/moyu?type=json"
        headers = {'Content-Type': "application/json"}
        try:
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('url'):
                    return json_data['url'], ReplyType.IMAGE_URL
                else:
                    logger.info(json_data)
                logger.info(f"moyu返回错误：{response.text}")
                return None, ReplyType.ERROR
        except Exception as e:
            logger.error(f"moyu接口异常：{e}")
            return None, ReplyType.ERROR

    def get_help_text(self, **kwargs):
        help_text = f"【摸鱼日历】获取摸鱼日历"
        return help_text