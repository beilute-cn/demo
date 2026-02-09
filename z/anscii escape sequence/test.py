import random
import string

import time

import inspect
from pathlib import Path
from datetime import datetime, timezone, timedelta


def log(message=""):
    # 获取调用者的帧

    if len(inspect.stack()) < 2:
        frame = inspect.currentframe()
    else:
        frame = inspect.currentframe().f_back

    print(
        f"[{datetime.now(timezone(timedelta(hours=8))):%Y-%m-%d %H:%M:%S.%f}]"
        "["
        f"{Path(frame.f_code.co_filename).name}, "
        f"{frame.f_code.co_name}(...), "
        f"@{frame.f_lineno}"
        "] > "
        f"{message}"
    )


import logging


class ColoredFormatter(logging.Formatter):
    """完整的带颜色格式化器"""

    # 颜色定义
    COLORS = {
        "DEBUG": "\033[36m",  # 青色
        "INFO": "\033[32m",  # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",  # 红色
        "CRITICAL": "\033[35m\033[1m",  # 紫色+粗体
    }
    RESET = "\033[0m"
    GREY = "\033[90m"
    BLUE = "\033[94m"

    def format(self, record):
        # 格式化时间（灰色）
        timestamp = self.formatTime(record, self.datefmt)
        time_str = f"{self.GREY}[{timestamp}.{record.msecs:03.0f}]{self.RESET}"

        # 格式化级别（彩色）
        level_color = self.COLORS.get(record.levelname, "")
        level_str = f"{level_color}[{record.levelname:^12}]{self.RESET}"

        # 格式化文件信息（蓝色）
        file_str = f"{self.BLUE}[{record.filename}, {record.funcName}(...), @{record.lineno}]{self.RESET}"

        # 获取消息
        message = record.getMessage()

        # 处理异常
        exc_text = ""
        if record.exc_info:
            exc_text = f"\n{self.formatException(record.exc_info)}"

        # 组合
        return f"{time_str}{level_str}{file_str} > {message}{exc_text}"


# 配置函数
def setup_colored_logging(level=logging.DEBUG):
    """配置带颜色的日志"""
    logging.basicConfig(level=level)

    for handler in logging.root.handlers:
        handler.setFormatter(ColoredFormatter(datefmt="%Y-%m-%d %H:%M:%S"))


# 使用
setup_colored_logging()


# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s.%(msecs)03d][%(filename)s, %(funcName)s(...), @%(lineno)d] > %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 5个基本日志级别函数
# logging.debug("调试信息 - 最详细的信息，通常只在诊断问题时使用")
# logging.info("普通信息 - 确认程序按预期运行")
# logging.warning("警告信息 - 表示发生了意外，但程序仍在运行")
# logging.error("错误信息 - 由于更严重的问题，程序某些功能无法执行")
# logging.critical("严重错误 - 严重错误，程序可能无法继续运行")


def divide(x, y):
    try:
        result = x / y
        return result
    except ZeroDivisionError:
        # logging.exception() - 自动记录异常堆栈信息（级别为 ERROR）
        logging.exception("除零错误发生")
        return None
    except Exception as e:
        # logging.error() 配合 exc_info=True 也可以记录堆栈
        logging.error(f"发生错误: {e}", exc_info=True)
        return None


# divide(10, 0)


# 确保密码包含大写、小写、数字和特殊字符
def strong_password(length=12):
    if length < 4:
        raise ValueError("密码长度至少为4")

    # 确保至少包含一个每种类型的字符
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]

    print(f"{password}")

    # 填充剩余长度
    all_chars = string.ascii_letters + string.digits + string.punctuation

    print(f"{all_chars}")

    password += random.choices(all_chars, k=length - 4)

    print(f"{password}")

    # 打乱顺序
    random.shuffle(password)

    print(f"{password}")

    return "".join(password)


# print(f"强密码: {strong_password(16)}")


print("test")


descriptions = {
    # 1.1 文本属性
    0: "重置所有属性",
    1: "粗体/加粗",
    2: "弱化/变暗",
    3: "斜体",
    4: "下划线",
    5: "慢速闪烁",
    6: "快速闪烁",
    7: "反转/反显",
    8: "隐藏/不可见",
    9: "删除线",
    10: "默认字体",
    # 11 - 19: "替代字体",
    20: "哥特体",
    21: "双下划线",
    # 取消
    22: "正常强度",
    23: "非斜体非哥特体",
    24: "非下划线",
    25: "非闪烁",
    27: "非反转",
    28: "非隐藏",
    29: "非删除线",
    # 1.2 标准前景色 (30-39)
    30: "黑色",
    31: "红色",
    32: "绿色",
    33: "黄色",
    34: "蓝色",
    35: "洋红/品红",
    36: "青色",
    37: "白色",
    38: "扩展前景色（256色/RGB）",
    39: "默认前景色",
    # 1.3 标准背景色 (40-49)
    40: "黑色背景",
    41: "红色背景",
    42: "绿色背景",
    43: "黄色背景",
    44: "蓝色背景",
    45: "洋红背景",
    46: "青色背景",
    47: "白色背景",
    48: "扩展背景色（256色/RGB）",
    49: "默认背景色",
    # 1.4 其他属性 (50-59)
    # 50: "保留",
    51: "框线",
    52: "圆圈",
    53: "上划线",
    54: "非框线非圆圈",
    55: "非上划线",
    # 56 - 59: "	保留",
    # 1.5 表意文字属性 (60-65)
    60: "表意文字下划线或右侧线",
    61: "表意文字双下划线或双右侧线",
    62: "表意文字上划线或左侧线",
    63: "表意文字双上划线或双左侧线",
    64: "表意文字着重标记",
    65: "表意文字属性关闭",
    # 1.6 高亮前景色 (90-97)
    90: "亮黑色（灰色）",
    91: "亮红色",
    92: "亮绿色",
    93: "亮黄色",
    94: "亮蓝色",
    95: "亮洋红",
    96: "亮青色",
    97: "亮白色",
    # 1.7 高亮背景色 (100-107)
    100: "亮黑色背景",
    101: "亮红色背景",
    102: "亮绿色背景",
    103: "亮黄色背景",
    104: "亮蓝色背景",
    105: "亮洋红背景",
    106: "亮青色背景",
    107: "亮白色背景",
}

section = {
    0: "1.1 文本属性",
    # 22: "取消",
    30: "1.2 标准前景色",
    40: "1.3 标准背景色",
    51: "1.4 其他属性",
    60: "1.5 表意文字属性",
    90: "1.6 高亮前景色",
    100: "1.7 高亮背景色",
}

cancel = {
    1: 22,  # "正常强度"
    2: 22,
    3: 23,  # "非斜体非哥特体"
    4: 24,  # "非下划线"
    5: 25,  # "非闪烁"
    6: 25,
    7: 27,  # "非反转"
    8: 28,  # "非隐藏"
    9: 29,  # "非删除线"
    # 11 - 19: 1 - 9,
    20: 23,
    21: 24,
    51: 54,
    52: 54,
    53: 55,
}


def call(f):
    # print("=" * 25, f.__doc__, "=" * 25)
    f()


def test():
    # call(f1)
    # call(f2)
    # call(f3)
    # call(f4)
    # call(f5)
    # call(f6)
    # call(f7)
    # call(f8)
    # call(f9)
    # call(f10)
    # call(f11)
    # call(f12)
    # call(f13)
    # call(f14)
    # call(f15)
    # call(f16)
    # call(f17)
    # call(f18)


def f1():
    "1. 文本样式和颜色 (SGR - Select Graphic Rendition)"

    if True:
        key_of_section = section.keys()
        value_of_cancel = cancel.values()

        for key, value in descriptions.items():

            if key in key_of_section:
                print("=" * 25, section[key], "=" * 25)

            if key in value_of_cancel:
                continue

            print(f"[{key:3}] <\033[{key}m{value}\033[0m>")

        print("=" * 25, "取消", "=" * 25)
        for key, value in cancel.items():
            print(
                f"[{value:3}] <\033[{key}m{descriptions[key]}> "
                f"<\033[{value}m{descriptions[value]}> "
                f"<\033[{key}m{descriptions[key]}\033[0m>"
            )

    call(f1_8)
    call(f1_9)


def f1_8():
    "1.8 256色模式"
    # 前景色        \033[38;5;<n>m
    # 背景色        \033[48;5;<n>m
    # 下划线颜色    \033[58;5;<n>m

    # 颜色索引 (n = 0-255)：
    #   0-7:    标准颜色
    #   8-15:   高亮颜色
    #   16-231: 216色调色板 (6×6×6 RGB)
    #       计算公式: 16 + 36 × r + 6 × g + b (r,g,b ∈ [0,5])
    #   232-255: 24级灰度

    # foreground and background

    # 标准颜色
    print("=" * 25, "标准颜色", "=" * 25)
    for i in range(7 + 1):
        for j in range(7 + 1):
            print(f"\033[38;5;{i};48;5;{j}m<{i},{j}>\033[0m", end="")
        print()

    # 高亮颜色
    print("=" * 25, "高亮颜色", "=" * 25)
    for i in range(8, 15 + 1):
        for j in range(8, 15 + 1):
            print(f"\033[38;5;{i};48;5;{j}m<{i:2},{j:2}>\033[0m", end="")
        print()

    # 216色调色板 (6×6×6 RGB)
    print("=" * 25, "216色调色板 (6×6×6 RGB)", "=" * 25)

    print("=" * 25, "前景色", "=" * 25)
    # for r in range(6):
    r = 0
    for g in range(6):
        for b in range(6):
            print(
                f"\033[38;5;{16+36*r+6*g+b}m好\033[0m",
                end="",
            )
        print()

    print("=" * 25, "背景色", "=" * 25)
    for r in range(6):
        # for g in range(6):
        g = 0
        for b in range(6):
            print(
                f"\033[48;5;{16+36*r+6*g+b}m好\033[0m",
                end="",
            )
        print()

    print("=" * 25, "下划线（无效果）", "=" * 25)
    for r in range(6):
        for g in range(6):
            # for b in range(6):
            b = 0
            print(
                f"\033[58;5;{16+36*r+6*g+b}m好\033[0m",
                end="",
            )
        print()


def f1_9():
    # 1.9 RGB 真彩色 (24位)
    print("=" * 25, "1.9 RGB 真彩色 (24位)", "=" * 25)
    # 前景色：\033[38;2;<r>;<g>;<b>m
    # 背景色：\033[48;2;<r>;<g>;<b>m
    # 下划线颜色：\033[58;2;<r>;<g>;<b>m
    # 其中 r, g, b ∈ [0, 255]

    print("=" * 25, "前景色", "=" * 25)
    # for r in range(0, 256, 8):
    r = 0
    for g in range(0, 256, 8):
        for b in range(0, 256, 8):
            print(
                f"\033[38;2;{r};{g};{b}m好\033[0m",
                end="",
            )
        print()

    print("=" * 25, "背景色", "=" * 25)
    for r in range(0, 256, 8):
        # for g in range(0, 256, 8):
        g = 0
        for b in range(0, 256, 8):
            print(
                f"\033[48;2;{r};{g};{b}m好\033[0m",
                end="",
            )
        print()

    print("=" * 25, "下划线（无效果）", "=" * 25)
    for r in range(0, 256, 8):
        for g in range(0, 256, 8):
            # for b in range(0, 256, 8):
            b = 0
            print(
                f"\033[58;2;{r};{g};{b}m好\033[0m",
                end="",
            )
        print()


def f2():
    "2. 光标控制"
    call(f2_1)
    call(f2_3)
    call(f2_4)


def f2_1():
    "2.1 光标移动（2.2 光标位置保存/恢复）"

    # 序列	功能	说明
    # \033[<n>A	光标上移	n 行（默认1）
    # \033[<n>B	光标下移	n 行（默认1）
    # \033[<n>C	光标右移	n 列（默认1）
    # \033[<n>D	光标左移	n 列（默认1）
    # \033[<n>E	光标移到下 n 行开头	默认1
    # \033[<n>F	光标移到上 n 行开头	默认1
    # \033[<n>G	光标移到第 n 列	绝对位置
    # \033[<row>;<col>H	光标移到指定位置	行;列（从1开始）
    # \033[<row>;<col>f	光标移到指定位置	同 H

    # \033[H	光标移到左上角	默认位置

    for r in range(40):
        for c in range(81):
            if c == 40:
                print("|", end="")
            print("-", end="")
        print(f"{r}")

    # ---------------------------------
    # print("\033[s", end="")
    print("\0337", end="")
    # ---------------------------------

    print("\033[20Aup", end="")
    print("\033[2Bdown", end="")
    print("\033[4Cright", end="")
    print("\033[9Dleft", end="")

    print("\033[1Ehead1", end="")
    print("\033[2Fhead2", end="")

    print("\033[41Gline 10", end="")  # 从1开始，可以覆盖原有的换行符

    print("\033[10;10H<10,10>", end="")
    print("\033[11;11f<11,11>", end="")

    # print("")  # 无换行，不刷新
    # while True:
    # pass

    # 2.2 光标位置保存/恢复
    # 序列	功能
    # \033[s	保存光标位置 (SCO)
    # \033[u	恢复光标位置 (SCO)
    # \0337	保存光标位置 (DEC)
    # \0338	恢复光标位置 (DEC)

    # ---------------------------------
    # print("\033[u")
    print("\0338")

    # ---------------------------------

    # print("\033[0m")


def f2_3():
    "2.3 光标显示"

    # vscode terminal/cygwin 默认显示，不闪烁（半个方块，选中实心，未选中空心）
    # window terminal 默认闪烁（竖线）

    # 序列	功能
    # \033[?25h	显示光标
    # \033[?25l	隐藏光标
    # \033[?12h	启用光标闪烁
    # \033[?12l	禁用光标闪烁

    print("显示光标（输入以继续...）\033[?25h", end="")
    input()
    print("隐藏光标（输入以继续...）\033[?25l", end="")
    input()

    # 隐藏光标后，闪烁无效
    print("\033[?25h", end="")

    print("启用光标闪烁（输入以继续...）\033[?12h", end="")
    input()
    print("禁用光标闪烁（输入以继续...）\033[?12l", end="")
    input()


def f2_4():
    "2.4 光标形状"

    # 闪烁
    print("\033[?25h\033[?12h", end="")
    # print("\033[?25h", end="")

    # wt 默认闪，对应正常
    # vsc/cygwin 默认不闪，开启闪烁后全闪

    # 序列	形状
    # \033[0 q	默认
    # \033[1 q	闪烁块
    # \033[2 q	稳定块
    # \033[3 q	闪烁下划线
    # \033[4 q	稳定下划线
    # \033[5 q	闪烁竖线
    # \033[6 q	稳定竖线

    desc = [
        "默认",
        "闪烁块",
        "稳定块",
        "闪烁下划线",
        "稳定下划线",
        "闪烁竖线",
        "稳定竖线",
    ]

    for i in range(len(desc)):
        print(f"{desc[i]}（输入以继续...）\033[{i} q", end="")
        input()

    # 配置不闪烁
    print("稳定块，配置不闪烁（输入以继续...）\033[2 q\033[?12l", end="")
    input()

    # 恢复默认
    print("\033[0 q", end="")


def f3():
    "3. 屏幕清除"
    call(f3_1)
    call(f3_2)


def f3_1():
    "3.1 清除屏幕"

    # 多行

    # 序列	功能
    # \033[J	清除从光标到屏幕末尾
    # \033[0J	清除从光标到屏幕末尾
    # \033[1J	清除从屏幕开头到光标
    # \033[2J	清除整个屏幕
    # \033[3J	清除整个屏幕及回滚缓冲区

    map = {
        "J": "清除从光标到屏幕末尾",
        "0J": "清除从光标到屏幕末尾",
        "1J": "清除从屏幕开头到光标",
        "2J": "清除整个屏幕",  # 有回滚内容
        "3J": "清除缓冲区",
        "2J\033[3J\033[H": "清除屏幕及缓冲区并回到顶部",
    }

    for key, value in map.items():
        # 输出多行字符
        print((string.ascii_lowercase + "\n") * 20)
        # 光标闪烁，移动到中间
        print("\033[?25h\033[?12h\033[5A\033[15C", end="", flush=True)
        time.sleep(3)
        print(f"\033[{key}")
        # print("=" * 50)
        # print(f"\033[3J", end="", flush=True)


def f3_2():
    "3.2 清除行"

    # 序列	功能
    # \033[K	清除从光标到行末
    # \033[0K	清除从光标到行末
    # \033[1K	清除从行开头到光标
    # \033[2K	清除整行

    map = {
        "K": "清除从光标到行末",
        "0K": "清除从光标到行末",
        "1K": "清除从行开头到光标",
        "2K": "清除整行",
    }

    for key, value in map.items():
        print(f"{value}: ")
        print("\t", "0123456789" * 2, end="")
        print(f"\033[?25h\033[?12h\033[15D", end="", flush=True)
        time.sleep(2)
        print(f"\033[{key}")


def f4():
    "4. 滚动"

    # 序列	功能
    # \033[<n>S	向上滚动 n 行，默认为1
    # \033[<n>T	向下滚动 n 行，默认为1
    # \033[<top>;<bottom>r	设置滚动区域

    # 滚动会改变缓冲区内容
    # 设定滚动区域后，光标在全屏幕的(1, 1)

    print("\033[1;20r", end="", flush=True)
    for i in range(1, 30):
        print(f"line {i+96}", flush=True)
        time.sleep(0.5)

    for i in range(3):
        n = random.randint(5, 10)
        for j in range(n):
            print(f"\033[T", end="", flush=True)
            time.sleep(0.5)
        for j in range(n):
            print(f"\033[S", end="", flush=True)
            time.sleep(0.5)

    # 等价
    print("\033[r", end="", flush=True)
    # print("\033[;r", end="", flush=True)


def f5():
    "5. 文本插入/删除"

    # 序列	功能
    # \033[<n>@	插入 n 个空格
    # \033[<n>P	删除 n 个字符，后面字符向前移动
    # \033[<n>X	擦除 n 个字符，空位
    # \033[<n>L	插入 n 行，当前行不截断，和之后的行，向下移动。所以与所在列无关
    # \033[<n>M	删除 n 行

    print("A" * 50)
    # 向左移动后测试
    print(string.digits, "\033[6Dabc")
    print(string.digits, "\033[6D\033[3@")
    print(string.digits, "\033[6D\033[3P")
    print(string.digits, "\033[6D\033[3X")

    for c in range(ord("B"), ord("H") + 1):
        print(chr(c) * 50)

    # 向上，向右移动后测试
    # print("\033[2A\033[6Cabcd", end="", flush=True)
    print("\033[2A\033[6C\033[3La", end="", flush=True)

    # 将光标移出改动的几行
    print("\033[10B")

    for c in range(ord("I"), ord("O") + 1):
        print(chr(c) * 50)
    print("\033[4A\033[6C\033[2Ma", end="", flush=True)

    print("\033[10B")


def f6():
    "6. 模式设置"
    # call(f6_1)
    call(f6_2)


def f6_1():
    "6.1 屏幕模式"
    # 序列	功能
    # \033[=0h	40×25 黑白
    # \033[=1h	40×25 彩色
    # \033[=2h	80×25 黑白
    # \033[=3h	80×25 彩色
    # \033[=4h	320×200 4色
    # \033[=5h	320×200 黑白
    # \033[=6h	640×200 黑白
    # \033[=7h	启用自动换行
    # \033[=13h	320×200 彩色
    # \033[=14h	640×200 16色
    # \033[=15h	640×350 黑白
    # \033[=16h	640×350 16色
    # \033[=17h	640×480 黑白
    # \033[=18h	640×480 16色
    # \033[=19h	320×200 256色

    # 终端模拟器不支持


import msvcrt


import subprocess
import sys
import time


def f6_2():
    "6.2 私有模式 (DEC Private Mode)"

    # \033[?<n>h

    # 序列  功能
    # 1     应用光标键模式
    # 3     132列模式
    # 4 	平滑滚动
    # 5     反显模式
    # 6     原点模式
    # 7     自动换行
    # 12	光标闪烁
    # 25	显示光标
    # 47	使用备用屏幕缓冲区
    # 1000  MOUSE_X10            鼠标报告
    # 1002  MOUSE_BTN            按钮事件跟踪
    # 1003  MOUSE_ANY            任意事件跟踪
    # 1004  FOCUS                焦点事件
    # 1005  MOUSE_UTF8           UTF-8 鼠标模式
    # 1006  MOUSE_SGR            SGR 鼠标模式
    # 1047  XTERM_SAVE_ALT       备用屏幕缓冲
    # 1048  XTERM_SAVE_CURSOR    保存光标
    # 1049	启用备用屏幕（保存光标
    # 2004	启用括号粘贴模式
    """
        上下右左
        
        cat
            h> ABCD
            l> 方向键
        cat -v
            h> ^[OA^[OB^[OC^[OD
            l> ^[[A^[[B^[[C^[[D
        od -An -tx1
            h>
                1b 4f 41
                1b 4f 42
                1b 4f 43
                1b 4f 44
            l>
                1b 5b 41
                1b 5b 42
                1b 5b 43
                1b 5b 44
        od -c
            h> 0000000 033   O   A 033   O   B 033   O   C 033   O   D 033   O   A  \n
            l> 0000000 033   [   A 033   [   B 033   [   C 033   [   D 033   [   A  \n
        xxd -g 1
            h> ABCDA
                00000000: 1b 4f 41 1b 4f 42 1b 4f 43 1b 4f 44 1b 4f 41 0a  .OA.OB.OC.OD.OA.
            l> 方向键
                00000000: 1b 5b 41 1b 5b 42 1b 5b 43 1b 5b 44 1b 5b 41 0a  .[A.[B.[C.[D.[A.
        hexdump -C
            h> ABCDA
                00000000  1b 4f 41 1b 4f 42 1b 4f  43 1b 4f 44 1b 4f 41 0a  |.OA.OB.OC.OD.OA.|
            l> 方向键
                00000000  1b 5b 41 1b 5b 42 1b 5b  43 1b 5b 44 1b 5b 41 0a  |.[A.[B.[C.[D.[A.|
        sed -n l
            h> ABCD
                \033OA\033OB\033OC\033OD$
            l> 方向键
                \033[A\033[B\033[C\033[D$
        
        printf '\033[?1h'
        echo -e '\033[?1h'
        tput smkx / rmkx
    """
    # 正常模式（模式 1 关闭）
    # 按键    cat 显示    十六进制    字符表示
    # ↑       ^[[A       1B 5B 41    ESC [ A
    # ↓       ^[[B       1B 5B 42    ESC [ B
    # →       ^[[C       1B 5B 43    ESC [ C
    # ←       ^[[D       1B 5B 44    ESC [ D

    # 应用模式（模式 1 开启）
    # 按键    cat 显示    十六进制    字符表示
    # ↑       ^[OA       1B 4F 41    ESC O A
    # ↓       ^[OB       1B 4F 42    ESC O B
    # →       ^[OC       1B 4F 43    ESC O C
    # ←       ^[OD       1B 4F 44    ESC O D

    # 按键	第一字节	第二字节	十六进制	十进制
    # ↑	0xE0	0x48	E0 48	224 72
    # ↓	0xE0	0x50	E0 50	224 80
    # →	0xE0	0x4D	E0 4D	224 77
    # ←	0xE0	0x4B	E0 4B	224 75

    # msvcrt.getch() 读取的是 Windows 原始输入，不受 VT100 转义序列影响
    # cat -v 读取的是终端处理后的输出，会受模式切换影响

    # ?1
    if False:
        r = b""
        print("\033[?1h")
        r += read()

        print("\033[?1l")
        r += read()

        print(f"{r}")

    # ?3
    if False:
        print("\033[?3h")
        print("a" * 150)

        print("\033[?3l")
        print("a" * 150)

    # 4
    if False:
        print("\033[?4h")
        for i in range(100):
            print(f"line {i}")
            time.sleep(0.05)

        print("\033[?4l")
        for i in range(100):
            print(f"line {i}")
            time.sleep(0.05)

    # ?5
    # wt支持
    # vscode无效
    if False:
        print("\033[?5h")
        print("hello world")
        input(">")

        print("\033[?5l")
        print("hello world")
        input(">")

    # windows terminal / command prompt
    # echo ^[[r
    #   第一个^[ 使用 Ctrl + [ 输入
    #   第二个[，是正常符号

    # ?6
    if False:
        # 光标闪烁
        print("\033[?25h\033[?12h", end="", flush=True)
        time.sleep(2)

        # 非原点模式，全屏滚动
        print("\033[?6l\033[r", end="", flush=True)
        time.sleep(2)

        for i in range(1, 20):
            print(f"line {i}")

        time.sleep(2)

        # 原点模式，滚动区域
        print("\033[?6h\033[5;10r", end="", flush=True)
        input(">")

        # 禁用原点模式，恢复全屏滚动，清屏
        print("\033[?6l\033[2J\033[3J\033[r", end="", flush=True)

    # ?7
    if False:
        print("\033[?7h", end="", flush=True)
        print("A" * 200)

        print("\033[?7l", end="", flush=True)
        print("B" * 200)

        # 开启自动换行
        print("\033[?7h", end="", flush=True)

    # vscode 支持
    # wt不支持
    # ?47
    if False:
        print("\033[?47h", end="", flush=True)
        print("启用备用屏幕缓冲区")
        input(">")

        print("\033[?47l", end="", flush=True)
        print("禁用备用屏幕缓冲区")
        input(">")

    # 1000
    if False:
        print("hello world")
        print("\033[?1000h", end="", flush=True)

        while True:
            key = msvcrt.getch()
            if key == b"q":
                break
            print(f"{key}")
            pass

    import msvcrt
    import os

    print("\033[?1000h\033[?1006h", end="", flush=True)

    stdin_fd = sys.stdin.fileno()
    msvcrt.setmode(stdin_fd, os.O_BINARY)

    while True:
        print(f"{os.read(stdin_fd, 1024)}")


"""
7. 键盘/输入
序列	功能
\033[<n>h	设置模式
\033[<n>l	重置模式
\033[2h	键盘锁定
\033[2l	键盘解锁
\033[4h	插入模式
\033[4l	替换模式
\033[12h	回显开
\033[12l	回显关
\033[20h	换行模式
\033[20l	正常模式
"""


def f7():
    # 2
    # 4
    # 直接在命令行演示，已删除的字符还会出现
    print("替换")
    print(f"{string.digits}")
    print("插入")
    print(f"{string.digits}\033[4h\033[5Dabcd\033[4l")

    # 12

    # 20
    print(f"换行\033[20h")
    print(string.digits * 20)
    print(f"正常\033[20l")
    print(string.digits * 20)


"""
8. 查询/报告
序列	功能	响应
\033[6n	查询光标位置	\033[<row>;<col>R
    从1开始
\033[5n	查询设备状态	\033[0n (正常)
    0 正常
    3 故障
\033[0c	查询设备属性	设备相关
    ^[[?61;4;6;7;14;21;22;23;24;28;32;42;52c
\033[c	查询设备代码	设备相关
    
"""


def f8():
    import sys

    # 响应回显到输入流
    if False:
        print("\033[6n", end="", flush=True)
        # 读取响应，通常格式为 \033[row;colR
        r = []
        while True:
            c = sys.stdin.read(1)
            r.append(c)
            if c == "R":
                break
        print(f"响应: {repr(r)}")

    import sys
    import msvcrt

    print("test\nabcd", end="", flush=True)
    # windows读取输入流

    print("\033[6n", end="", flush=True)

    response = ""

    while True:
        # 检查是否有按键输入
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if isinstance(ch, bytes):
                ch = ch.decode("utf-8", errors="ignore")
            response += ch
            if ch == "R":
                break
    print(f"{response=}")

    # 当变量是转义序列时，直接输出变量和与名称一起输出不同
    # x = f"\033[6n"
    # print(f"{x}")
    # print(f"{x=}")


"""
9. 标签/制表符
序列	功能
\033H	在当前位置设置制表符
\033[<n>I	向前移动 n 个制表位
\033[<n>Z	向后移动 n 个制表位
\033[0g	清除当前列的制表符
\033[3g	清除所有制表符
"""


def f9():
    pass


"""
10. 字符集选择
序列	功能
\033(0	选择线条绘制字符集 (G0)
\033(B	选择 ASCII 字符集 (G0)
\033)0	选择线条绘制字符集 (G1)
\033)B	选择 ASCII 字符集 (G1)


a       ▒
b       ␉
c       ␌
d       ␍
e       ␊
f       °
g       ±
h       ␤
i       ␋
j       ┘
k       ┐
l       ┌
m       └
n       ┼
o       ⎺
p       ⎻
q       ─
r       ⎼
s       ⎽
t       ├
u       ┤
v       ┴
w       ┬
x       │
y       ≤
z       ≥


只有小写，并列时有变化
"""


def f10():
    for i in string.ascii_lowercase:
        print(f"{i}\t\033(0{i}\033(B")

    """
    ---   ---   ---  ---  --- 1
    |            |          | 2
    |            |          | 3
    |---  ---   -|-  --- ---| 4
    |            |          | 5
    |            |          | 6
    ---   ---   ---  ---  --- 7
    """
    line = "\033(0"
    anscii = "\033(B"
    no = 1

    print(f"{line}lqwqk{anscii}\t({no})")
    no += 1
    print(f"{line}x x x{anscii}\t({no})")
    no += 1
    print(f"{line}tqnqu{anscii}\t({no})")
    no += 1
    print(f"{line}x x x{anscii}\t({no})")
    no += 1
    print(f"{line}mqvqj{anscii}\t({no})")


"""
11. 窗口操作
序列	功能
\033[1t	取消最小化窗口
\033[2t	最小化窗口
# \033[3;<x>;<y>t	移动窗口到 x,y
# \033[4;<h>;<w>t	调整窗口大小（像素）
# \033[5t	窗口置顶
# \033[6t	窗口置底
# \033[7t	刷新窗口
# \033[8;<h>;<w>t	调整窗口大小（字符）
# \033[9;0t	取消最大化
# \033[9;1t	最大化窗口
# \033[10;0t	取消全屏
# \033[10;1t	全屏
# \033[11t	查询窗口状态
\033[18t	查询窗口大小（字符）
# \033[19t	查询屏幕大小（字符）
# \033[20t	查询窗口图标标签
# \033[21t	查询窗口标题
"""


def f11():
    print("\033[2t")
    time.sleep(1)
    print("\033[1t")


"""
12. 标题设置
序列	功能
# \033]0;<title>\007	设置窗口标题和图标
# \033]1;<title>\007	设置图标标题
# \033]2;<title>\007	设置窗口标题
"""


def f12():
    # print("\033]0;test\007")
    # print("\033]1;test\007")
    # print("\033]2;test\007")
    pass


"""
13. 超链接 (OSC 8)
\033]8;;<URL>\007<文本>\033]8;;\007

或使用 ST (String Terminator):
\033]8;;<URL>\033\\<文本>\033]8;;\033\\

"""


def f13():
    print("\033]8;;https://www.baidu.com\007文本\033]8;;\007")
    print("\033]8;;https://www.baidu.com\033\\文本\033]8;;\033\\")
    pass


"""

14. 通知 (OSC 9 - iTerm2/其他)
\033]9;<消息>\007

"""


def f14():
    print(f"\033]9;消息\007")


"""

15. 进度条 (OSC 9;4 - ConEmu/Windows Terminal)
\033]9;4;<state>;<progress>\007

state: 0=无进度, 1=不确定, 2=正常, 3=错误, 4=暂停
progress: 0-100


"""


def f15():
    print("\033]9;4;0;20\007")


"""
16. 剪贴板操作 (OSC 52)
\033]52;<clipboard>;<data>\007

clipboard: c=剪贴板, p=主选择, s=次选择
data: base64 编码的文本
"""


def f16():
    # 1234 --base64--> MTIzNA==
    print("\033]52;c;MTIzNA==\007")
    # print("\033]52;p;test\007")
    # print("\033]52;s;test\007")


"""
17. 软重置
序列	功能
\033[!p	软重置终端
\033c	完全重置终端 (RIS)

"""


def f17():
    # print("\033[!p")
    # print("\033c")
    pass


"""
18. 其他控制序列
序列	功能
\007	响铃 (BEL)
\010	退格 (BS)
\011	水平制表符 (HT)
\012	换行 (LF)
\013	垂直制表符 (VT)
\014	换页 (FF)
\015	回车 (CR)
\033D	索引 (向下滚动)
\033E	下一行 (NEL)
\033M	反向索引 (向上滚动)
\033Z	识别终端

"""


def f18():
    print("1234\0105")


def read():
    key = b""

    while not msvcrt.kbhit():
        pass

    key += msvcrt.getch()
    if key in (b"\x00", b"\xe0"):
        key += msvcrt.getch()
    return key


test()
print("\033[0m")
