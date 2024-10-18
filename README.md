# ChatBot

本项目使用了 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 作为连接 QQ 的方式

本项目使用了 [WeChatFerry](https://github.com/lich0821/WeChatFerry) 作为连接微信的方式(挂载稍有难度, 故默认关闭微信连接)

# 挂载项目

## 使用 `win10、11 python310 ` 环境, 其余环境均未测试

1. 拉取仓库
2. 直接运行`main.py`文件, 会弹出`config.py`文件
3. 根据注释提示完善`config.py`文件(初次运行不建议开启`debug`, 容易扫不到登入二维码)
4. 安装所有依赖(请注意一定要先执行第二步运行`main.py`, 此处有元编程运用)
   `pip install -r requirements.txt`
   若想启用虚拟环境在此处启用即可
   后期可能改自动安装, 目前在开发阶段, 还请手动安装
5. 重新启动`main.py`, 登入 QQ(和微信)
6. 重新启动`main.py`, 即可使用

#### 用户分为`root绝对权限`, `管理员`, `高级权限`和`普通用户`四种

1. `root权限`: 极少数个人项功能, 比如日记等(日记插件暂未上传 github, 因为与作者服务器高度耦合, 无复用性)目前 root 权限只有这一个功能
   > **_截止 2023/12/21 仍无需配置 root 权限_**
2. `管理员`: 添加在`config.py`中的`admin_list`和`wx_admin_list`中, 添加后需热重载才生效

   1. 收发通知, 获取报错信息
   2. 管理员使用单独的两个管理员线程, 相对也不那么拥挤
   3. 强烈建议至少有一个, 否则报错信息回丢失, 难以及时处理

3. `高级权限`: 添加后即刻生效

   1. 可使用被隐藏的有点违规的人格, 具体在`config.py`中的`default_prompt_permission_password`字段附近查看详细设置
   2. 可切换自己的`session`配置(大白话: 可以使用 gpt4, 如果有的话)

4. `普通用户`: 所有配置都为默认, 可切换合法人格

> 管理员和高级权限相互独立, 可存在管理员无高级权限, 也存在高级权限无管理员

> tips: 默认插件里绝大部分仅为作者个人喜好, 故一些不能直接使用的插件是默认关闭的, 具体可在源码搜索`TODO`自行查询(感觉也没什么复用性)
>
> QQ 登入是非阻塞的, 故第一次登入后需重启项目。微信登入是阻塞的, 但请不要在登入完成之前进行热重载

> [微信需安装 3.9.2.23 版本](https://github.com/lich0821/WeChatFerry/releases/tag/v39.0.11), 故默认关闭。**强烈建议在服务器环境下实验**, 你也不希望你的电脑微信版本倒退吧
>
> 有需要请下载后安装, 登入, 设置里取消自动更新, 打开自动下载(默认就是打开状态)
>
> 然后退出微信后台(注意是退出线程, 不是最小化, 因为会进行 dll 注入)
>
> 然后前往本项目`.plugins\wcferry\main.py`中设置`enabled`为`True`, 即可启用
>
> **注意每次重启程序时, 请确保无后台微信进程, 否则无法正常收发消息且难以有提示!**
>
> 由于 qq 和微信共用一套命令系统, 故微信有一些命令暂未完善, 但都做了简单的反馈
>
> QQ 微信可同时登入, 逻辑共用, 数据不互通

---

# 当前已有插件的优先级(感叹号开头为命令):

| 优先级 | 名称                       | 备注                             |
| ------ | -------------------------- | -------------------------------- |
| -100   | \_\_log 日志               | > 双下划线开头为高耦合项         |
| -99    | \_\_config 配置文件        | > 基本没插件不需要这几个吧       |
| -98    | \_\_threadctl 线程池管理   | > 但他们也符合插件编写规范       |
| ------ | **基本连接**               |                                  |
| 1      | QQbot 连接 qq              | 基于`go-cqhttp`                  |
| 2      | weChat 连接微信            | 基于`WeChatFerry`                |
| 10     | OpenAi 连接 gpt            | 基于官方文档                     |
| ------ | **qq 消息处理**            |                                  |
| 100    | qq 文本消息处理            |                                  |
| 101    | qq 撤回消息处理            | 默认发送撤回消息, 使对方无效撤回 |
| ------ | **微信消息处理**           |                                  |
| 150    | weChat 文本消息处理        | 与 qq 基本相同                   |
| ------ | **命令类**                 |                                  |
| 201    | `!cmd`查看所有命令         | 命令以感叹号开头, 中英文均可     |
| 202    | `!help`查看自定义帮助信息  |                                  |
| 203    | `!send`与管理员发起对话    | 管理员请用`!send <qq 号> <内容>` |
| 204    | `!alarm`定时提醒           | 需要特殊 api, 请注意             |
| 205    | `!default`查看所有场景设置 | 可自定义写入`config.py`          |
| 206    | `!reset`设置当前场景预设   | 每个用户独立维护一个`session`    |
| 207    | `!reload`热重载命令        | 管理员命令                       |
| 208    | `!add`好友添加处理         | 管理员命令                       |
| 209    | `!history`查看聊天历史记录 | 程序本身未提供数据库, 关闭即清空 |
| 210    | `!talk`和 gpt 对话         | 管理员指导/单轮配置切换          |
| 211    | `!spoof`假借他人之名对话   | 虚拟转发的群聊记录               |
| 212    | `!note`备忘录              | 简单的备忘录记录, 标注为键值对   |
| ------ | **图片相关命令**           | 注意优先级                       |
| 250    | `!diary`日记命令           | 私人不上传                       |
| 251    | `!水印`照片添加水印        | 方便青年大学习写班级姓名         |
| 252    | `!图片`随机图片获取        | 免费 api 实现                    |
| ------ | **工具类**                 |                                  |
| 1000   | 敏感词屏蔽                 |                                  |
| 1001   | QQ 长消息处理              |                                  |
| ------ | **终止符**                 |                                  |
| 10000  | endCmd 命令终止符          |                                  |

### 当前进度:

~~QQ 正常使用, 正在阅读微信连接方法。该死的英语四级, 项目咕一会(灬 ꈍ ꈍ 灬)~~

~~四级挂了, 淦~~

~~正在接微信。支持微信 QQ 同时登入, 且用同一套逻辑(甚至数据也可以互通, 目前暂时为全隔离状态, 可自己接)~~

基本写完了, 没啥大 bug, 小 bug 知道的暂时都解决了, 欢迎提交 issue(虽然没啥可能)

# 插件编写规范

# 1. 主线程流程

启动主程序后

1. 加载 log 和 config
2. 加载所有[插件基类](#2-插件基类编写规范plugin)
3. while True: time.sleep(0xFF)不返回

   如果意外出错, 在这里做配置保存等

由于主线程的插件特性, 可直接删去`gocqOnQQ`文件夹而不报错, 但实际因为内部耦合度大, 并不建议这么做

实际上只有双下划线开头的不可删除, 其余`./plugins`下的文件并非必须项

[当前已有插件的优先级](#当前已有插件的优先级:)

# 2. 插件基类编写规范(`Plugin`)

插件目录结构应如下

- ChatBot
  - `plugins`
    - `__config`
      - `__init__.py`
      - `Events.py`
      - `main.py`
    - ... ...
    - `yourPluginName`
      - `__init__.py`
      - `config-template.py`
      - `Events.py`
      - `main.py`
      - `requirements.txt`
    - ... ...

1. `__init__.py`(空文件)和`main.py`不可省略, 其余可省略。

   但如果日后有计划使用此配置, 可提前用同名空文件占位

2. 项目采用了一些元编程元素, 在`__config.py`中按插件优先级读取`config-template.py`, `Events.py`, `requirements.txt`中的内容写入主线程的同名文件中。以`##### {plugin.name=} {plugin.path=} #####`作为分隔。

   程序启动时会更新上述文件, 但不更新`config.py`(用户填写, 并在程序启动时创建该文件)

3. 插件基类应当有`__init__`, `on_reload`, `on_stop`三个函数, 分别为**初始化**, **热重载**和**程序异常尝试保存**

4. 每个插件基类同时最多应当只有主线程创建的**唯一实例**

5. 插件中的函数应被`@Plugin.on()`注册, 否则函数不会被`self.emit()`直接触发
   (`@Plugin.on()`可简写为`@on()`, `emit()`由于方便日志记录等原因, 出于可读性考虑不支持简写)

6. 尽量使用封装的`emit()`函数调用其他插件的函数

   当然在 Plugin 中拥有`plugin_list`保存了插件列表, 按优先级排序, 请自行确保安全调用

插件的`main.py`编写示例:

```python
from Models.Plugins import *
from plugins.__config.Events import *

@register(
    description="输出hello world",  # 插件描述
    version="1.0.0",                # 插件版本
    author="For_Lin0601",           # 作者
    priority=500  # 负数应预留给程序运行必须项, 请尽量不要出现重复的优先级, 否则函数触发顺序不易确定
)
class Config(Plugin):  # 注意类名会作为一些 不安全 函数的标识, 尽管在书写这些不安全函数时做了声明, 但还希望类名不重复

    def __init__(self):
        if self.is_first_init():  # 判断程序是否为第一次启动
            self.config = None
        else:
            self.config = Plugin.get_reload_config("config")
            # `get_reload_config()`不传参则返回热重载前设定的整个字典
            # 此函数背后字典将于热重载结束后清空, 推荐在热重载`on_reload`中通过`set_reload_config(key, value)`存入

    # 事件应写在`Events.py`中
    # GetConfig__ = "get_config__"
    # """获取配置

    #     kwargs:
    #         None

    #     return:
    #         config: ModuleType  # 配置模块(以 value = config.key 读取)
    # """

    @on(GetConfig__)  # 双下划线结尾表示必阻塞事件, 即只应当有此事件开发者自己注册此事件, 供外部`self.emit(GetConfig__)`使用
    def get_config(self, event: EventContext,  **kwargs):  # 函数名实际上没关系, 但建议规范命名, 以及不和`Plugin`中的函数名冲突
        """获取配置列表"""
        event.prevent_postorder()
        event.return_value = self.config  # 插件不显式`return`
        # 返回值请自行保存到`event.return_value`中, 主线程不做任何合法性判断

    # 若希望程序启动和重载完后都触发, 可以使用如下连续两个`@on()`装饰同一个函数
    @on(PluginsLoadingFinished)  # 插件首次加载时触发(程序启动时)
    @on(PluginsReloadFinished)  # 插件重载完成时触发
    def get_Config(self, event: EventContext,  **kwargs):
        from Event import GetConfig__
        # 此处除了主线程必须项必然出现, 其余项可能在程序第一次运行后才创建
        # 故此处强烈建议动态导入所需变量。否则可能需要多次`关闭-启动`项目才可导入所有变量
        # 另外的, 如果有两个或更多插件之间的变量相互引用, 相互触发, 会导致完全无法读取变量
        # 目前如果删去Events.py中除主线程必须项以外所有变量, 程序大约会在`关闭-启动`四次左右完全读取所有变量
        # `关闭-启动`是指主线程进入到while True: time.sleep(0xFF)后关闭程序, 启动程序等待主线程进入while True: time.sleep(0xFF)
        config = self.emit(GetConfig__)  # `emit`返回值请看`Events.py`中对应的注解
        # `emit`后续参数只接受`**kwargs`, 且在响应插件内打包为`kawrgs`参数
        # 优点是响应插件内必解包`kwargs`, 可做类型声明

    def on_reload(self):
        self.set_reload_config("config", self.config)
        # 此处会将配置写入`Plugin.__reload_config__`字典, 此字典将在热重载完成后才清空
        # 故如果有配置不需要热重载, 可在此暂存
        # 同时在`def __init__`中判断`self.is_first_init()`来决定设置配置或读取配置

    def on_stop(self):
        # 程序异常停止时调用, 比如数据库存储, 日志记录等
        # 无意外不调用
        pass
```
