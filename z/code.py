#!/usr/bin/env python3
"""ANSI 转义序列完整演示"""

class ANSI:
    """ANSI 转义序列常量"""
    
    # 重置
    RESET = '\033[0m'
    
    # 样式
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色前景
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # 背景色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # 光标控制
    CURSOR_UP = lambda n=1: f'\033[{n}A'
    CURSOR_DOWN = lambda n=1: f'\033[{n}B'
    CURSOR_FORWARD = lambda n=1: f'\033[{n}C'
    CURSOR_BACK = lambda n=1: f'\033[{n}D'
    CURSOR_POS = lambda row, col: f'\033[{row};{col}H'
    
    # 清除
    CLEAR_SCREEN = '\033[2J'
    CLEAR_LINE = '\033[2K'
    CLEAR_TO_END = '\033[0J'
    CLEAR_TO_START = '\033[1J'
    
    # 光标显示
    CURSOR_SHOW = '\033[?25h'
    CURSOR_HIDE = '\033[?25l'
    
    # 保存/恢复
    CURSOR_SAVE = '\033[s'
    CURSOR_RESTORE = '\033[u'
    
    @staticmethod
    def rgb(r, g, b, bg=False):
        """RGB 颜色"""
        code = 48 if bg else 38
        return f'\033[{code};2;{r};{g};{b}m'
    
    @staticmethod
    def color256(n, bg=False):
        """256 色"""
        code = 48 if bg else 38
        return f'\033[{code};5;{n}m'

def demo_styles():
    """演示文本样式"""
    print("\n=== 文本样式 ===")
    print(f"{ANSI.BOLD}粗体文本{ANSI.RESET}")
    print(f"{ANSI.DIM}弱化文本{ANSI.RESET}")
    print(f"{ANSI.ITALIC}斜体文本{ANSI.RESET}")
    print(f"{ANSI.UNDERLINE}下划线文本{ANSI.RESET}")
    print(f"{ANSI.REVERSE}反转文本{ANSI.RESET}")
    print(f"{ANSI.STRIKETHROUGH}删除线文本{ANSI.RESET}")

def demo_colors():
    """演示颜色"""
    print("\n=== 标准颜色 ===")
    colors = [
        ('黑色', ANSI.BLACK),
        ('红色', ANSI.RED),
        ('绿色', ANSI.GREEN),
        ('黄色', ANSI.YELLOW),
        ('蓝色', ANSI.BLUE),
        ('洋红', ANSI.MAGENTA),
        ('青色', ANSI.CYAN),
        ('白色', ANSI.WHITE),
    ]
    for name, code in colors:
        print(f"{code}■■■ {name}{ANSI.RESET}")
    
    print("\n=== 亮色 ===")
    bright_colors = [
        ('亮黑', ANSI.BRIGHT_BLACK),
        ('亮红', ANSI.BRIGHT_RED),
        ('亮绿', ANSI.BRIGHT_GREEN),
        ('亮黄', ANSI.BRIGHT_YELLOW),
        ('亮蓝', ANSI.BRIGHT_BLUE),
        ('亮洋红', ANSI.BRIGHT_MAGENTA),
        ('亮青', ANSI.BRIGHT_CYAN),
        ('亮白', ANSI.BRIGHT_WHITE),
    ]
    for name, code in bright_colors:
        print(f"{code}■■■ {name}{ANSI.RESET}")

def demo_256_colors():
    """演示 256 色"""
    print("\n=== 256 色调色板 ===")
    
    # 标准色 0-15
    print("标准色 (0-15):")
    for i in range(16):
        print(f"{ANSI.color256(i)}█{ANSI.RESET}", end='')
        if i == 7:
            print()
    print("\n")
    
    # 216 色立方体 16-231
    print("216 色立方体 (16-231):")
    for i in range(216):
        print(f"{ANSI.color256(i + 16)}█{ANSI.RESET}", end='')
        if (i + 1) % 36 == 0:
            print()
    
    # 灰度 232-255
    print("\n灰度 (232-255):")
    for i in range(24):
        print(f"{ANSI.color256(i + 232)}█{ANSI.RESET}", end='')
    print()

def demo_rgb():
    """演示 RGB 真彩色"""
    print("\n=== RGB 真彩色 ===")
    
    # 渐变
    print("红色渐变:")
    for i in range(0, 256, 8):
        print(f"{ANSI.rgb(i, 0, 0)}█{ANSI.RESET}", end='')
    print()
    
    print("绿色渐变:")
    for i in range(0, 256, 8):
        print(f"{ANSI.rgb(0, i, 0)}█{ANSI.RESET}", end='')
    print()
    
    print("蓝色渐变:")
    for i in range(0, 256, 8):
        print(f"{ANSI.rgb(0, 0, i)}█{ANSI.RESET}", end='')
    print()
    
    print("彩虹:")
    for i in range(32):
        r = int(127.5 * (1 + __import__('math').sin(i * 0.2)))
        g = int(127.5 * (1 + __import__('math').sin(i * 0.2 + 2)))
        b = int(127.5 * (1 + __import__('math').sin(i * 0.2 + 4)))
        print(f"{ANSI.rgb(r, g, b)}█{ANSI.RESET}", end='')
    print()

def demo_cursor():
    """演示光标控制"""
    print("\n=== 光标控制 ===")
    print("保存位置...", end='', flush=True)
    print(ANSI.CURSOR_SAVE, end='')
    import time
    time.sleep(1)
    
    print("\n移动光标...")
    time.sleep(1)
    
    print(ANSI.CURSOR_RESTORE, end='')
    print(" 恢复位置!")

def demo_combinations():
    """演示组合效果"""
    print("\n=== 组合效果 ===")
    print(f"{ANSI.BOLD}{ANSI.RED}粗体红色{ANSI.RESET}")
    print(f"{ANSI.UNDERLINE}{ANSI.GREEN}下划线绿色{ANSI.RESET}")
    print(f"{ANSI.BOLD}{ANSI.ITALIC}{ANSI.BLUE}粗斜体蓝色{ANSI.RESET}")
    print(f"{ANSI.BG_YELLOW}{ANSI.BLACK}黄底黑字{ANSI.RESET}")
    print(f"{ANSI.BOLD}{ANSI.WHITE}{ANSI.BG_RED}粗体白字红底{ANSI.RESET}")

def demo_hyperlink():
    """演示超链接"""
    print("\n=== 超链接 (部分终端支持) ===")
    url = "https://github.com"
    text = "GitHub"
    print(f"\033]8;;{url}\007{text}\033]8;;\007")

def demo_title():
    """演示标题设置"""
    print("\n=== 设置窗口标题 ===")
    print("\033]0;ANSI 演示程序\007", end='')
    print("窗口标题已设置为: ANSI 演示程序")

if __name__ == '__main__':
    print(f"{ANSI.BOLD}ANSI 转义序列完整演示{ANSI.RESET}")
    print
