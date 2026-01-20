import sys
import ctypes
from ctypes import wintypes
import time

# Windows API 常量
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_VIRTUAL_TERMINAL_INPUT = 0x0200
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

# 事件类型
KEY_EVENT = 0x0001
MOUSE_EVENT = 0x0002

# 鼠标事件标志
FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001
RIGHTMOST_BUTTON_PRESSED = 0x0002
FROM_LEFT_2ND_BUTTON_PRESSED = 0x0004
MOUSE_MOVED = 0x0001
DOUBLE_CLICK = 0x0002
MOUSE_WHEELED = 0x0004


# 结构体定义
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


def main():
    kernel32 = ctypes.windll.kernel32

    # 获取控制台句柄
    h_stdin = kernel32.GetStdHandle(STD_INPUT_HANDLE)
    h_stdout = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    # 启用虚拟终端处理（输出）
    mode = wintypes.DWORD()
    kernel32.GetConsoleMode(h_stdout, ctypes.byref(mode))
    mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(h_stdout, mode)

    # 启用鼠标输入
    kernel32.GetConsoleMode(h_stdin, ctypes.byref(mode))
    mode.value |= ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS
    kernel32.SetConsoleMode(h_stdin, mode)

    # 清屏并显示标题
    print("\033[2J\033[H", end="")
    print("=" * 70)
    print(" " * 15 + "Windows 控制台鼠标事件接收")
    print("=" * 70)
    print("\n点击、拖动、移动鼠标")
    print("按 'q' 键退出\n")

    # 启用 ANSI 鼠标模式（可选，主要用 Windows API）
    print("\033[?1000h\033[?1006h", end="", flush=True)

    event_count = 0
    input_record = INPUT_RECORD()
    events_read = wintypes.DWORD()

    try:
        while True:
            # 检查是否有输入事件
            num_events = wintypes.DWORD()
            kernel32.GetNumberOfConsoleInputEvents(h_stdin, ctypes.byref(num_events))

            if num_events.value == 0:
                time.sleep(0.01)
                continue

            # 读取输入事件
            if kernel32.ReadConsoleInputW(
                h_stdin, ctypes.byref(input_record), 1, ctypes.byref(events_read)
            ):
                if events_read.value > 0:
                    # 处理鼠标事件
                    if input_record.EventType == MOUSE_EVENT:
                        mouse = input_record.Event.MouseEvent
                        event_count += 1

                        # 解析按钮状态
                        buttons = []
                        if mouse.dwButtonState & FROM_LEFT_1ST_BUTTON_PRESSED:
                            buttons.append("左键")
                        if mouse.dwButtonState & RIGHTMOST_BUTTON_PRESSED:
                            buttons.append("右键")
                        if mouse.dwButtonState & FROM_LEFT_2ND_BUTTON_PRESSED:
                            buttons.append("中键")

                        # 解析事件类型
                        event_type = "点击"
                        if mouse.dwEventFlags & MOUSE_MOVED:
                            event_type = "移动"
                        elif mouse.dwEventFlags & DOUBLE_CLICK:
                            event_type = "双击"
                        elif mouse.dwEventFlags & MOUSE_WHEELED:
                            wheel_delta = ctypes.c_short(
                                mouse.dwButtonState >> 16
                            ).value
                            event_type = f"滚轮({'上' if wheel_delta > 0 else '下'})"

                        button_str = "+".join(buttons) if buttons else "无"

                        print(
                            f"[{event_count:3d}] {event_type:8s} "
                            f"按钮={button_str:12s} "
                            f"位置=({mouse.dwMousePosition.X:3d},{mouse.dwMousePosition.Y:3d})"
                        )

                    # 处理键盘事件
                    elif input_record.EventType == KEY_EVENT:
                        key = input_record.Event.KeyEvent
                        if key.bKeyDown and key.uChar == "q":
                            break

    except KeyboardInterrupt:
        print("\n\n中断...")

    finally:
        print("\033[?1000l\033[?1006l", end="", flush=True)
        print(f"\n总共接收 {event_count} 个鼠标事件")


if __name__ == "__main__":
    main()
