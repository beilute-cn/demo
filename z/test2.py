# 导入
import string
import ctypes
from ctypes import wintypes
from enum import Enum, IntFlag


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


# 起始
print(">" * 50)


# 缩进
class Tab:
    format = "\t"
    count = 0

    def tab(self):
        self.count = self.count + 1

    def untab(self):
        if self.count > 0:
            self.count = self.count - 1

    def __str__(self):
        return self.format * self.count


tab = Tab()


# 加载
kernel = ctypes.windll.kernel32


kernel.GetStdHandle.argtypes = [wintypes.DWORD]
kernel.GetStdHandle.restype = wintypes.HANDLE

# 定义函数原型

# ReadConsole 字符
test_ReadConsole = False  # WA
# ReadConsoleInput 事件
test_ReadConsoleInput = True  # WA
# ReadConsoleInputEx
# ReadConsoleOutput
# ReadConsoleOutputAttribute
# ReadConsoleOutputCharacter (读取控制台输出字符)


# ReadConsole 在 Windows API 中实际上是一个宏，真实的函数名是：
# ReadConsoleA - ANSI 版本
# ReadConsoleW - Unicode 版本
# 需要使用 ReadConsoleW 或 ReadConsoleA，而不是 ReadConsole。

kernel.ReadConsoleA.argtypes = [
    wintypes.HANDLE,
    wintypes.LPVOID,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.LPVOID,
]
kernel.ReadConsoleA.restype = wintypes.BOOL


class u_char(ctypes.Union):
    _fields_ = [
        ("Unicode_char", wintypes.WCHAR),
        ("ascii_char", wintypes.CHAR),
    ]


class control_key(IntFlag):
    NONE = 0
    RIGHT_ALT_PRESSED = 0x0001  # 	按下右 Alt 键。
    LEFT_ALT_PRESSED = 0x0002  # 	按下左 Alt 键。
    RIGHT_CTRL_PRESSED = 0x0004  # 	按下右 Ctrl 键。
    LEFT_CTRL_PRESSED = 0x0008  # 	按下左 Ctrl 键。
    SHIFT_PRESSED = 0x0010  #
    NUMLOCK_ON = 0x0020  # NUM LOCK 灯已打开。
    SCROLLLOCK_ON = 0x0040  # 	SCROLL LOCK 灯已打开。
    CAPSLOCK_ON = 0x0080  # 	CAPS LOCK 灯已打开。
    ENHANCED_KEY = 0x0100  # 密钥已增强。 请参阅 备注。

    def all(self):
        map = {
            control_key.RIGHT_ALT_PRESSED.value: "右Alt",
            control_key.LEFT_ALT_PRESSED.value: "Alt",  # "左Alt",
            control_key.RIGHT_CTRL_PRESSED.value: "右Ctrl",
            control_key.LEFT_CTRL_PRESSED.value: "Ctrl",  # "左Ctrl",
            control_key.SHIFT_PRESSED.value: "Shift",
            control_key.NUMLOCK_ON.value: "NUM LOCK",
            control_key.SCROLLLOCK_ON.value: "SCROLL LOCK",
            control_key.CAPSLOCK_ON.value: "CAPS LOCK",
            control_key.ENHANCED_KEY.value: "增强",
        }
        r = []
        v = self.value
        for key, value in map.items():
            if v & key:
                r.append(value)
                v &= ~key
        if v:
            print(f"\033[31m还有未识别的控制键<{hex(v)}>\033[0m")
        return r

    def __str__(self):
        return str(self.all())


class event_parse:
    def parse(self):
        pass


class which_member:
    def which():
        pass


class key_event_record(event_parse, ctypes.Structure):
    _fields_ = [
        ("b_key_down", wintypes.BOOL),
        ("w_repeat_count", wintypes.WORD),
        ("w_virtual_key_code", wintypes.WORD),
        ("w_virtual_scan_code", wintypes.WORD),
        ("u_char", u_char),
        ("dw_control_key_state", wintypes.DWORD),
    ]

    class mouse:

        def __init__(self):
            self.status = 0
            self.button = 0
            self.x = 0
            self.y = 0
            self.count = 0

        def parse(self, key):
            char = key.u_char.ascii_char
            match self.status:
                case 0:
                    if char == b"\033":
                        self.status = 1
                    else:
                        self.status = 0
                        return False
                case 1:
                    if char == b"[":
                        self.status = 2
                    else:
                        self.status = 0
                        return False
                case 2:
                    if char == b"M":
                        self.status = 3
                    else:
                        self.status = 0
                        return False
                case 3:
                    # 忽略shift
                    # 忽略按下和释放
                    if key.w_virtual_key_code == 16:
                        pass
                    else:
                        if self.count:
                            # print(key)
                            self.button = ord(char) - 32
                            self.status = 4
                            self.count = 0
                        else:
                            self.count = 1
                case 4:
                    if key.w_virtual_key_code == 16:
                        pass
                    else:
                        if self.count:
                            self.x = ord(char) - 32
                            self.status = 5
                            self.count = 0
                        else:
                            self.count = 1
                case 5:
                    if key.w_virtual_key_code == 16:
                        pass
                    else:
                        if self.count:
                            self.y = ord(char) - 32
                            print(f"mouse<{self.button}, {self.x}, {self.y}>")
                            self.status = 0
                            self.count = 0
                        else:
                            self.count = 1
            return True

        def __str__(self):
            return f"""\
{tab}按钮:{self.button}
{tab}X坐标:{self.x}
{tab}Y坐标:{self.y}\
"""

    mouse = mouse()

    def parse(self):
        """
        print("格式: \\033[M<btn><x><y>")
        print()
        print("组成部分:")
        print("  \\033    = ESC 字符 (0x1B, 27)")
        print("  [       = 左方括号 (0x5B, 91)")
        print("  M       = 字母 M (0x4D, 77)")
        print("  <btn>   = 按钮码 + 32 (单字节 ASCII 字符)")
        print("  <x>     = X 坐标 + 32 (单字节 ASCII 字符)")
        print("  <y>     = Y 坐标 + 32 (单字节 ASCII 字符)")
        """

        # \033[M<btn><x><y> 格式的鼠标事件解析
        if key_event_record.mouse.parse(self):
            return

        user32 = ctypes.windll.user32
        # 获取按键名称
        buffer_anscii = ctypes.create_string_buffer(20)
        ctypes.memset(ctypes.addressof(buffer_anscii), 0, ctypes.sizeof(buffer_anscii))
        if user32.GetKeyNameTextA(self.w_virtual_scan_code << 16, buffer_anscii, 20):

            print(
                f""
                + f"<"
                + (f"\033[0m" if self.b_key_down else "\033[90m")
                + f"{buffer_anscii.value.decode('utf-8', errors='ignore')}"
                + " \033[32m["
                + " + ".join(control_key(self.dw_control_key_state).all())
                + "]"
                + f"\033[0m>"
            )
        else:
            logging.warning(f"无按键名称")

    def __str__(self):
        return f"{"↓" if self.b_key_down else "↑"}, {self.w_virtual_key_code}, {self.w_virtual_scan_code}, {self.u_char.ascii_char.decode('utf-8', errors='ignore')}<{self.u_char.ascii_char.hex()}>, {control_key(self.dw_control_key_state)}"
        return f"""\
{tab}按键：{"按下" if self.b_key_down else "释放"}
{tab}重复次数：{self.w_repeat_count}
{tab}虚拟键码：{self.w_virtual_key_code}
{tab}扫描码：{self.w_virtual_scan_code}
{tab}字符：{self.u_char.ascii_char.decode('utf-8', errors='ignore')}<{self.u_char.ascii_char.hex()}>
{tab}控制键状态：{control_key(self.dw_control_key_state)}\
"""

        return f"""\
{tab}b_key_down={self.b_key_down}
{tab}wVirtuw_repeat_countalKeyCode={self.w_repeat_count}
{tab}w_virtual_key_code={self.w_virtual_key_code})
{tab}w_virtual_scan_code={self.w_virtual_scan_code}
{tab}u_char={self.u_char.ascii_char}
{tab}dw_control_key_state={self.dw_control_key_state}\
"""


class coord(ctypes.Structure):
    _fields_ = [
        ("X", wintypes.SHORT),
        ("Y", wintypes.SHORT),
    ]


class mouse_event(ctypes.Structure):
    _fields_ = [
        ("dw_mouse_position", coord),
        ("dw_button_state", wintypes.DWORD),
        ("dw_control_key_state", wintypes.DWORD),
        ("dw_event_flags", wintypes.DWORD),
    ]

    def parse(self):
        print(
            f"Mouse Position: ({self.dw_mouse_position.X}, {self.dw_mouse_position.Y})"
        )
        print(f"Button State: {hex(self.dw_button_state)}")
        print(f"Control Key State: {control_key(self.dw_control_key_state)}")
        print(f"Event Flags: {hex(self.dw_event_flags)}")
        print("=" * 50)


class window_buffer_size_event(ctypes.Structure):
    _fields_ = [
        ("dw_size", coord),
    ]

    def parse(self):
        print(f"<\033[35m<{self.dw_size.X} * {self.dw_size.Y}\033[0m>")


class menu_event(ctypes.Structure):
    _fields_ = [
        ("dw_command_id", wintypes.UINT),
    ]


class focus_event(event_parse, ctypes.Structure):
    _fields_ = [
        ("b_set_focus", wintypes.BOOL),
    ]

    def parse(self):
        print(
            f""
            + f"<"
            + (f"\033[0m获得焦点" if self.b_set_focus else "\033[90m失去焦点")
            + f"\033[0m>"
        )


class event(ctypes.Union):
    _fields_ = [
        ("key_event", key_event_record),
        ("mouse_event", mouse_event),
        ("window_buffer_size_event", window_buffer_size_event),
        ("menu_event", menu_event),
        ("focus_event", focus_event),
    ]


class event_type(IntFlag, Enum):
    KEY_EVENT = 0x0001
    MOUSE_EVENT = 0x0002
    MENU_EVENT = 0x0008
    FOCUS_EVENT = 0x0010
    WINDOW_BUFFER_SIZE_EVENT = 0x0004

    def __str__(self):
        mapping = {
            0x0010: "焦点事件",
            0x0001: "键盘事件",
            0x0008: "菜单事件",
            0x0002: "鼠标事件",
            0x0004: "窗口缓冲区大小事件",
        }
        return mapping.get(self.value, f"未知事件<{self.value}>")


class _input_record(event_parse, which_member, ctypes.Structure):
    _fields_ = [
        ("event_type", wintypes.WORD),
        ("event", event),
    ]

    def which(self):
        match self.event_type:
            case event_type.FOCUS_EVENT.value:
                return self.event.focus_event
            case event_type.KEY_EVENT.value:
                return self.event.key_event
            case event_type.MENU_EVENT.value:
                return self.event.menu_event
            case event_type.MOUSE_EVENT.value:
                return self.event.mouse_event
            case event_type.WINDOW_BUFFER_SIZE_EVENT.value:
                return self.event.window_buffer_size_event
            case _:
                return None

    def parse(self):
        t = self.which()
        if t:
            t.parse()

    def __str__(self):
        return str(self.which())
        print(f"{self.event_type}")
        tab.tab()
        t = str(self.which())
        tab.untab()

        return f"""\
{tab}事件类型： {event_type(self.event_type)}
{tab}事件：
{t}\
"""

        return f"""\
{tab}event_type = {event_type(self.event_type).name}
{tab}event =
{t}\
"""


kernel.ReadConsoleInputA.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(_input_record),
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
]
kernel.ReadConsoleInputA.restype = wintypes.BOOL

# mode = wintypes.DWORD()
stdin = kernel.GetStdHandle(-10)
# kernel.GetConsoleMode(stdin, ctypes.byref(mode))
# print(mode)

# ENABLE_VIRTUAL_TERMINAL_INPUT = 0x0200
# kernel.SetConsoleMode(stdin, mode.value | ENABLE_VIRTUAL_TERMINAL_INPUT)


if test_ReadConsole:
    # 缓冲区大小
    size = wintypes.DWORD(20)
    buffer = ctypes.create_string_buffer(size.value)
    # 实际读取长度
    length = wintypes.DWORD()

    while True:
        # ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
        # length.value = 0
        flag = kernel.ReadConsoleA(
            stdin,
            buffer,
            size,
            ctypes.byref(length),
            None,
        )
        print(f"返回值：{flag}，长度：{length}，内容：{buffer.value}")


def char_name(char):
    if char == "\r":
        return "enter"
    elif char == "\x08":
        return "backspace"
    elif char == "\t":
        return "tab"
    elif char == "\x1b":
        return "esc"
    elif char == " ":
        return "space"
    elif char in string.printable:
        return char
    else:
        return None


if False:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    # 获取按键名称
    buffer_anscii = ctypes.create_string_buffer(100)
    buffer_anscii_2 = ctypes.create_string_buffer(100)
    buffer_unicode = ctypes.create_unicode_buffer(100)

    for i in range(1 << 9):
        ctypes.memset(ctypes.addressof(buffer_anscii), 0, ctypes.sizeof(buffer_anscii))
        ctypes.memset(
            ctypes.addressof(buffer_anscii_2), 0, ctypes.sizeof(buffer_anscii_2)
        )
        t = 0
        t += user32.GetKeyNameTextA(i << 16, buffer_anscii, 100)
        t += user32.GetKeyNameTextA(
            user32.MapVirtualKeyW(i, 0) << 16 | (1 << 24), buffer_anscii_2, 100
        )
        if t:
            print(f"{i:3} ->\t{buffer_anscii.value!r:20}{buffer_anscii_2.value!r:20}")


# 部分快捷键被vscode拦截，Ctrl + Shift + 2 可以
# 大写锁定，数字锁定，滚动锁定等状态只在wt有效，是种状态
# 仅按控制键，在wt可以检测到
# vscode在，输入后，即认为全部释放
# wt在实际释放时，才接收到
# 总是偶数

"""
        左键    右键    滚轮    移动
1000    20-23   22-23   60/61
1002
1003                            43  

"""
if test_ReadConsoleInput:
    try:
        # 开鼠标

        # 1. X10 鼠标协议 9
        # 2. UTF-8 鼠标协议 1005
        # 3. SGR 鼠标协议 1006
        # 4. URXVT 鼠标协议 1015

        # 1000
        # 1001 高亮
        # 1002 拖拽
        # 1003 移动
        n = [1006, 1002]

        for i in n:
            print(f"\033[?{i}h", end="", flush=True)

        size = wintypes.DWORD(10)
        buffer = (_input_record * size.value)()
        length = wintypes.DWORD()
        while True:
            # ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
            # length.value = 0
            flag = kernel.ReadConsoleInputA(
                stdin,
                buffer,
                size,
                ctypes.byref(length),
            )

            # print(f"返回值：{flag}, 长度：{length}，内容：")
            # tab.tab()
            for i in range(length.value):
                x = buffer[i]

                # if (
                # 0
                # and (x.event_type == event_type.KEY_EVENT.value)
                # and (x.event.key_event.u_char.ascii_char == b"q")
                # ):
                # print("\033[!p", end="", flush=True)
                # exit(0)

                # print(x.event.key_event.w_virtual_scan_code, end=" ", flush=True)
                x.parse()
                # print(x)
            # tab.untab()
            # print("=" * 50)
    except KeyboardInterrupt:
        for i in n:
            print(f"\033[?{i}l\033[0m", end="", flush=True)
        print("KeyboardInterrupt")

print("<" * 50)
