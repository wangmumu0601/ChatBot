

import Events
from Models.Plugins import *


@register(
    description="结尾指令, 若到大啊此处则表明无命令响应",
    version="1.0.0",
    author="For_Lin0601",
    priority=10000
)
class EndCommand(Plugin):

    @on(GetQQPersonCommand)
    @on(GetQQGroupCommand)
    def cmd_end(self, event: EventContext, **kwargs):
        message: str = kwargs["message"]
        event.prevent_postorder()
        self.emit(Events.GetCQHTTP__).sendPersonMessage(
            user_id=kwargs["sender_id"],
            message=f"[bot]err: 无命令响应: [!{message}]"
        )