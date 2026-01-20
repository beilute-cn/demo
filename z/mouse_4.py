import ctypes
from ctypes import wintypes
import time

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

MOUSE_EVENT = 0x0002
KEY_EVENT = 0x0001
MOUSE_WHEELED = 0x0004

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class MOUSE_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ("dwMousePosition", COORD),
        ("dwButtonState", wintypes.DWORD),
        ("dwControlKeyState", wintypes.DWORD),
        ("dwEventFlags", wintypes.DWORD)
    ]

class KEY_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ("bKeyDown", wintypes.BOOL),
        ("wRepeatCount", wintypes.WORD),
        ("wVirtualKeyCode", wintypes.WORD),
        ("wVirtualScanCode", wintypes.WORD),
        ("uChar", wintypes.WCHAR),
        ("dwControlKeyState", wintypes.DWORD)
    ]

class EventUnion(ctypes.Union):
    _fields_ = [("KeyEvent", KEY_EVENT_RECORD), ("MouseEvent", MOUSE_EVENT_RECORD)]

class INPUT_RECORD(ctypes.Structure):
    _fields_ = [("EventType", wintypes.WORD), ("Event", EventUnion)]

def main():
    kernel32 = ctypes.windll.kernel32
    
    h_stdin = kernel32.GetStdHandle(STD_INPUT_HANDLE)
    h_stdout = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    
    old_mode = wintypes.DWORD()
    kernel32.GetConsoleMode(h_stdin, ctypes.byref(old_mode))
    kernel32.SetConsoleMode(h_stdin, ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS)
    
    out_mode = wintypes.DWORD()
    kernel32.GetConsoleMode(h_stdout, ctypes.byref(out_mode))
    kernel32.SetConsoleMode(h_stdout, out_mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    
    print("\033[2J\033[H")
    print("=" * 80)
    print(" " * 25 + "滚轮事件详细信息")
    print("=" * 80)
    print("\n滚动鼠标滚轮，查看详细的事件数据")
    print("按 'q' 退出\n")
    
    input_record = INPUT_RECORD()
    events_read = wintypes.DWORD()
    event_num = 0
    
    try:
        while True:
            num = wintypes.DWORD()
            kernel32.GetNumberOfConsoleInputEvents(h_stdin, ctypes.byref(num))
            
            if num.value == 0:
                time.sleep(0.01)
                continue
            
            if kernel32.ReadConsoleInputW(h_stdin, ctypes.byref(input_record), 1, ctypes.byref(events_read)):
                if events_read.value == 0:
                    continue
                
                if input_record.EventType == KEY_EVENT:
                    key = input_record.Event.KeyEvent
                    if key.bKeyDown and key.uChar.lower() == 'q':
                        break
                
                if input_record.EventType == MOUSE_EVENT:
                    mouse = input_record.Event.MouseEvent
                    
                    if mouse.dwEventFlags & MOUSE_WHEELED:
                        event_num += 1
                        
                        # 原始数据
                        button_state = mouse.dwButtonState
                        
                        # 提取滚轮增量
                        wheel_delta = ctypes.c_short(button_state >> 16).value
                        
                        # 低16位（按钮状态）
                        low_word = button_state & 0xFFFF
                        
                        print(f"\n{'='*80}")
                        print(f"事件 #{event_num}")
                        print(f"{'='*80}")
                        print(f"原始 dwButtonState: 0x{button_state:08X} ({button_state})")
                        print(f"  高16位 (滚轮):    0x{button_state >> 16:04X} ({wheel_delta})")
                        print(f"  低16位 (按钮):    0x{low_word:04X} ({low_word})")
                        print(f"\n滚轮增量: {wheel_delta}")
                        print(f"方向: {'向上 ↑' if wheel_delta > 0 else '向下 ↓'}")
                        print(f"格数: {abs(wheel_delta) // 120}")
                        print(f"位置: ({mouse.dwMousePosition.X}, {mouse.dwMousePosition.Y})")
                        print(f"事件标志: 0x{mouse.dwEventFlags:04X}")
                        print(f"控制键状态: 0x{mouse.dwControlKeyState:08X}")
    
    except KeyboardInterrupt:
        print("\n\n中断")
    
    finally:
        kernel32.SetConsoleMode(h_stdin, old_mode)
        print(f"\n总共 {event_num} 个滚轮事件")

if __name__ == "__main__":
    main()
