from qg_botsdk import BOT, Model
import sqlite3
import yaml
import holodex
import restream

file_path = 'config.yaml'

with open(file_path, 'r') as f:
    config = yaml.safe_load(f)


def serach_key(user_id):
    conn = sqlite3.connect('rtmp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM rtmp_key WHERE user_id = ?", (user_id,))
    key = cursor.fetchone()
    cursor.close()
    conn.close()
    return key


def add_key(user_id, key):
    conn = sqlite3.connect('rtmp.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO rtmp_key (user_id, key) VALUES (?, ?)", (user_id, key))
    conn.commit()
    cursor.close()
    conn.close()


def edit_key(user_id, key):
    conn = sqlite3.connect('rtmp.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE rtmp_key SET key = ? WHERE user_id = ?", (key, user_id))
    conn.commit()
    cursor.close()
    conn.close()


# 连接到数据库（如果数据库不存在，它将被创建）
conn = sqlite3.connect('rtmp.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS rtmp_key (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    key TEXT
                )''')

conn.commit()
cursor.close()
conn.close()

# 创建全局会话对象检查消息是否来自于同一个对话


class Session:
    def __init__(self):
        self.response = None
        self.live_id = None
        self.session_active = False
        self.id = None


session = Session()


def deliver(data: Model.MESSAGE):   # 创建接收@消息事件的函数并绑定数据模型
    if session.session_active:
        if "退出" in data.treated_msg:
            session.session_active = False
            data.reply('已退出会话')
        elif data.treated_msg.isdigit():
            session.live_id = int(data.treated_msg)-1
            video_id = holodex.get_live_info(
                session.live_id, session.response)
            data.reply('获取直播成功，正在启动直播')
            user_key = serach_key(data.author.id)
            if user_key:
                data.reply('检测存在私信密钥，正在使用私信密钥')
                restream.start_live(video_id, user_key)
            else:
                data.reply('未检测到私信密钥，请先私信机器人发送密钥')

        else:
            data.reply('有进行中的会话，输入"退出"退出会话')
    else:
        if "查询直播" in data.treated_msg:
            session.response = holodex.live('stream', 'Hololive')
            result_str = holodex.get_live(session.response)
            data.reply(result_str)
            session.session_active = True
            session.id = data.author.id
        else:
            data.reply('没有进行中的会话，输入"查询直播"查询直播')


def dm_function(data: Model.DIRECT_MESSAGE):  # 创建接收私信消息事件的函数并绑定数据模型
    if 'txSecret' in data.treated_msg:
        user_key = serach_key(data.author.id)
        if user_key:
            edit_key(data.author.id, data.treated_msg)
            data.reply('已修改直播密钥')
        else:
            add_key(data.author.id, data.treated_msg)
            data.reply('已储存直播密钥')
    else:
        data.reply('您输入的好像不是准确的直播密钥')


bot = BOT(bot_id=config['bot_id'],
          bot_token=config['bot_token'])  # 实例化SDK核心类
bot.bind_msg(deliver)
bot.bind_dm(on_dm_function=dm_function)
bot.start()  # 开始运行机器人
