import ctypes
from ctypes import wintypes
import time

# ========== 常量 ==========
STD_INPUT_HANDLE = -10
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_EXTENDED_FLAGS = 0x0080
KEY_EVENT = 0x0001
MOUSE_EVENT = 0x0002

# 虚拟键码映射
VK_NAMES = {
    0x08: "BACKSPACE",
    0x09: "TAB",
    0x0D: "ENTER",
    0x1B: "ESC",
    0x20: "SPACE",
    0x21: "PAGE_UP",
    0x22: "PAGE_DOWN",
    0x23: "END",
    0x24: "HOME",
    0x25: "LEFT",
    0x26: "UP",
    0x27: "RIGHT",
    0x28: "DOWN",
    0x2D: "INSERT",
    0x2E: "DELETE",
    0x70: "F1",
    0x71: "F2",
    0x72: "F3",
    0x73: "F4",
    0x74: "F5",
    0x75: "F6",
    0x76: "F7",
    0x77: "F8",
    0x78: "F9",
    0x79: "F10",
    0x7A: "F11",
    0x7B: "F12",
}

# 控制键状态
SHIFT_PRESSED = 0x0010
LEFT_CTRL_PRESSED = 0x0008
RIGHT_CTRL_PRESSED = 0x0004
LEFT_ALT_PRESSED = 0x0002
RIGHT_ALT_PRESSED = 0x0001

# 鼠标按钮
FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001
RIGHTMOST_BUTTON_PRESSED = 0x0002
FROM_LEFT_2ND_BUTTON_PRESSED = 0x0004

# 鼠标事件
MOUSE_MOVED = 0x0001
DOUBLE_CLICK = 0x0002
MOUSE_WHEELED = 0x0004


# ========== 结构体 ==========
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


class KEY_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ("bKeyDown", wintypes.BOOL),
        ("wRepeatCount", wintypes.WORD),
        ("wVirtualKeyCode", wintypes.WORD),
        ("wVirtualScanCode", wintypes.WORD),
        ("uChar", wintypes.WCHAR),
        ("dwControlKeyState", wintypes.DWORD),
    ]


class MOUSE_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ("dwMousePosition", COORD),
        ("dwButtonState", wintypes.DWORD),
        ("dwControlKeyState", wintypes.DWORD),
        ("dwEventFlags", wintypes.DWORD),
    ]


class EventUnion(ctypes.Union):
    _fields_ = [("KeyEvent", KEY_EVENT_RECORD), ("MouseEvent", MOUSE_EVENT_RECORD)]


class INPUT_RECORD(ctypes.Structure):
    _fields_ = [("EventType", wintypes.WORD), ("Event", EventUnion)]


# ========== 辅助函数 ==========
def get_key_name(vk_code, char):
    """获取按键名称"""
    if char and char.isprintable():
        return f"'{char}'"
    return VK_NAMES.get(vk_code, f"VK_0x{vk_code:02X}")


def get_modifiers(state):
    """获取修饰键"""
    mods = []
    if state & (LEFT_CTRL_PRESSED | RIGHT_CTRL_PRESSED):
        mods.append("Ctrl")
    if state & (LEFT_ALT_PRESSED | RIGHT_ALT_PRESSED):
        mods.append("Alt")
    if state & SHIFT_PRESSED:
        mods.append("Shift")
    return "+".join(mods)


def get_mouse_buttons(state):
    """获取鼠标按钮状态"""
    buttons = []
    if state & FROM_LEFT_1ST_BUTTON_PRESSED:
        buttons.append("左键")
    if state & RIGHTMOST_BUTTON_PRESSED:
        buttons.append("右键")
    if state & FROM_LEFT_2ND_BUTTON_PRESSED:
        buttons.append("中键")
    return "+".join(buttons) if buttons else "无"


# ========== 主程序 ==========
def main():
    k32 = ctypes.windll.kernel32
    h_stdin = k32.GetStdHandle(STD_INPUT_HANDLE)

    # 保存并设置模式
    old_mode = wintypes.DWORD()
    k32.GetConsoleMode(h_stdin, ctypes.byref(old_mode))
    k32.SetConsoleMode(h_stdin, ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS)

    print("=" * 70)
    print("增强版输入监听器")
    print("=" * 70)
    print("按 ESC 退出\n")

    record = INPUT_RECORD()
    read = wintypes.DWORD()
    event_count = 0
    last_mouse_state = 0

    try:
        while True:
            if k32.ReadConsoleInputW(
                h_stdin, ctypes.byref(record), 1, ctypes.byref(read)
            ):
                if read.value == 0:
                    continue

                event_count += 1
                timestamp = time.strftime("%H:%M:%S")

                # 键盘事件
                if record.EventType == KEY_EVENT:
                    key = record.Event.KeyEvent
                    if key.bKeyDown:
                        key_name = get_key_name(key.wVirtualKeyCode, key.uChar)
                        mods = get_modifiers(key.dwControlKeyState)

                        output = f"[{timestamp}] [{event_count:4d}] 键盘: "
                        if mods:
                            output += f"{mods}+"
                        output += key_name

                        print(output)

                        if key.wVirtualKeyCode == 0x1B:  # ESC
                            break

                # 鼠标事件
                elif record.EventType == MOUSE_EVENT:
                    mouse = record.Event.MouseEvent
                    x, y = mouse.dwMousePosition.X, mouse.dwMousePosition.Y
                    state = mouse.dwButtonState
                    flags = mouse.dwEventFlags

                    # 按钮状态变化
                    if state != last_mouse_state and flags == 0:
                        buttons = get_mouse_buttons(state)
                        action = "按下" if state > last_mouse_state else "释放"
                        print(
                            f"[{timestamp}] [{event_count:4d}] 鼠标: {action} {buttons} 位置=({x},{y})"
                        )
                        last_mouse_state = state

                    # 双击
                    elif flags & DOUBLE_CLICK:
                        print(
                            f"[{timestamp}] [{event_count:4d}] 鼠标: 双击 位置=({x},{y})"
                        )

                    # 滚轮
                    elif flags & MOUSE_WHEELED:
                        delta = ctypes.c_short(state >> 16).value
                        direction = "↑" if delta > 0 else "↓"
                        print(
                            f"[{timestamp}] [{event_count:4d}] 鼠标: 滚轮{direction} 位置=({x},{y})"
                        )

                    # 移动（带按钮）
                    elif flags & MOUSE_MOVED and state != 0:
                        buttons = get_mouse_buttons(state)
                        print(
                            f"[{timestamp}] [{event_count:4d}] 鼠标: 拖动 {buttons} 位置=({x},{y})"
                        )

    except KeyboardInterrupt:
        print("\n\n程序被中断")

    finally:
        k32.SetConsoleMode(h_stdin, old_mode)
        print(f"\n总共捕获 {event_count} 个事件")
        print("控制台模式已恢复")


if __name__ == "__main__":
    main()
