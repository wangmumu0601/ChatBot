
import json
import re

import Events
from Models.Plugins import *

NOTE_FILE = os.path.join(os.path.dirname(__file__), "note.json")


@register(
    description="简单的备忘录[n, note]",
    version="1.0.0",
    author="For_Lin0601",
    priority=212
)
class NoteCommand(Plugin):

    def __init__(self):
        self.load_notes()

    def on_reload(self):
        self.load_notes()

    def load_notes(self):
        """加载备忘录"""
        if os.path.exists(NOTE_FILE):
            with open(NOTE_FILE, "r", encoding="utf-8") as f:
                self.notes = json.load(f)
        else:
            self.notes = {}

    def save_notes(self):
        """保存备忘录"""
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)

    def get_note_by_user_and_key(self, user_id, note_key):
        """获取用户的备忘录"""
        if user_id in self.notes:
            return self.notes[user_id].get(note_key, f"[bot]err: 备忘录不存在: `{note_key}`")
        else:
            return "[bot] 无备忘录"

    def get_notes_for_user(self, user_id):
        """获取用户的备忘录"""
        if user_id in self.notes:
            return self.notes[user_id]
        else:
            return {}

    def set_notes_for_user(self, user_id, notes):
        """设置用户的备忘录"""
        self.notes[user_id] = notes
        self.save_notes()

    def add_note(self, user_id, note_key, note_content):
        """添加备忘录, 禁止重复"""
        notes = self.get_notes_for_user(user_id)
        if note_key in notes:
            return f"[bot] 备忘录`{note_key}`已存在, 如需修改请用`!note e {note_key} {note_content[:10]}...`"
        notes[note_key] = note_content
        self.set_notes_for_user(user_id, notes)
        return f"[bot] 已添加备忘录: `{note_key}`: {note_content[:10]}..."

    def edit_note(self, user_id, note_key, new_content):
        """编辑备忘录"""
        notes = self.get_notes_for_user(user_id)
        if note_key in notes:
            notes[note_key] = new_content
            self.set_notes_for_user(user_id, notes)
            return f"[bot] 已编辑备忘录: `{note_key}`"
        else:
            return f"[bot] 备忘录不存在: `{note_key}`"

    def delete_note(self, user_id, note_key):
        """删除备忘录"""
        notes = self.get_notes_for_user(user_id)
        if note_key in notes:
            del notes[note_key]
            self.set_notes_for_user(user_id, notes)
            return f"[bot] 已删除备忘录: `{note_key}`"
        else:
            return f"[bot] 备忘录不存在: `{note_key}`"

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["note"] = {
            "is_admin": False,
            "alias": ["n", "note"],
            "summary": "简单的备忘录",
            "usage": (
                "!note\n"
                " - 查看所有备忘录\n"
                "!note <备忘录字段>\n"
                " - 查看某条备忘录\n"
                "!note a <备忘录字段> <备忘录内容>\n"
                " - 添加备忘录, 注意`备忘录字段`不能出现空格, `备忘录字段`不能重复\n"
                "!note e <备忘录字段> <备忘录内容>\n"
                " - 编辑备忘录, 注意`备忘录字段`不能出现空格\n"
                "!note d <备忘录字段>\n"
                " - 删除备忘录"
            ),
            "description": (
                "好多零碎的片段可以在此记录, 但由于机器人有一定不稳定性, 请勿将敏感信息存入备忘录。注意`a`,`e`,`d`命令前后必须加上空格"
            )
        }

    def normalize(self, message):
        """参数归一化"""
        message = message.strip()
        pattern = r'^n[^a-zA-Z]+'
        if not (re.search(pattern, message) or message == "n" or message.startswith("note")):
            return False
        if message.startswith("note"):
            note_list = message[4:].strip().split(maxsplit=3)
        elif message.startswith("n "):
            note_list = message[2:].strip().split(maxsplit=3)
        else:
            note_list = message[1:].strip().split(maxsplit=3)
        note_list = [n for n in note_list if n]
        return note_list

    @on(GetQQPersonCommand)
    def cmd_note_person(self, event: EventContext, **kwargs):
        note_list = self.normalize(kwargs['message'])
        if note_list is False:
            return
        event.prevent_postorder()

        user_id = kwargs["sender_id"]
        note_user_id = f"person_{user_id}"

        if len(note_list) == 0:
            reply = self.get_notes_for_user(note_user_id)
            # 转字符串
            if len(reply) == 0:
                reply = "[bot] 无备忘录"
            else:
                reply = "\n".join(
                    [f"[{i+1}] `{k}` - {v}" for i, (k, v) in enumerate(reply.items())])
        elif len(note_list) == 1:
            note_key = note_list[0]
            reply = self.get_note_by_user_and_key(note_user_id, note_key)
        elif note_list[0] == "a":
            note_key = note_list[1]
            note_content = " ".join(note_list[2:])
            reply = self.add_note(note_user_id, note_key, note_content)
        elif note_list[0] == "e":
            note_key = note_list[1]
            note_content = " ".join(note_list[2:])
            reply = self.edit_note(note_user_id, note_key, note_content)
        elif note_list[0] == "d":
            note_key = note_list[1]
            reply = self.delete_note(note_user_id, note_key)
        else:
            reply = f"[bot]err: 意外的参数: `{' '.join(note_list)}`, 请用`!cmd note`获取帮助"

        self.emit(Events.GetCQHTTP__).sendPersonMessage(user_id, reply)

    @on(GetQQGroupCommand)
    def cmd_note_group(self, event: EventContext, **kwargs):
        note_list = self.normalize(kwargs['message'])
        if note_list is False:
            return
        event.prevent_postorder()
        self.emit(Events.GetCQHTTP__).sendGroupMessage(
            kwargs["group"], "[bot] 群聊暂不支持此命令~")

    @on(GetWXCommand)
    def cmd_note_wx(self, event: EventContext, **kwargs):
        note_list = self.normalize(kwargs['command'])
        if note_list is False:
            return
        event.prevent_postorder()

        user_id = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        note_user_id = f"wx_{user_id}"

        if len(note_list) == 0:
            reply = self.get_notes_for_user(note_user_id)
            # 转字符串
            if len(reply) == 0:
                reply = "[bot] 无备忘录"
            else:
                reply = "\n".join(
                    [f"[{i+1}] `{k}` - {v}" for i, (k, v) in enumerate(reply.items())])
        elif len(note_list) == 1:
            note_key = note_list[0]
            reply = self.get_note_by_user_and_key(note_user_id, note_key)
        elif note_list[0] == "a":
            note_key = note_list[1]
            note_content = " ".join(note_list[2:])
            reply = self.add_note(note_user_id, note_key, note_content)
        elif note_list[0] == "e":
            note_key = note_list[1]
            note_content = " ".join(note_list[2:])
            reply = self.edit_note(note_user_id, note_key, note_content)
        elif note_list[0] == "d":
            note_key = note_list[1]
            reply = self.delete_note(note_user_id, note_key)
        else:
            reply = f"[bot]err: 意外的参数: `{' '.join(note_list)}`, 请用`!cmd note`获取帮助"

        self.emit(Events.GetWCF__).send_text(reply, user_id)
