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
MOUSE_HWHEELED = 0x0008

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
    print("=" * 70)
    print(" " * 20 + "滚轮测试专用")
    print("=" * 70)
    print("\n请滚动鼠标滚轮（向上/向下）")
    print("按 'q' 退出\n")
    
    input_record = INPUT_RECORD()
    events_read = wintypes.DWORD()
    
    wheel_up_count = 0
    wheel_down_count = 0
    total_delta = 0
    
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
                    
                    # 只处理滚轮事件
                    if mouse.dwEventFlags & MOUSE_WHEELED:
                        # 提取滚轮增量（高16位）
                        wheel_delta = ctypes.c_short(mouse.dwButtonState >> 16).value
                        
                        total_delta += wheel_delta
                        
                        if wheel_delta > 0:
                            wheel_up_count += 1
                            direction = "↑ 向上"
                            symbol = "▲"
                        else:
                            wheel_down_count += 1
                            direction = "↓ 向下"
                            symbol = "▼"
                        
                        # 计算滚动格数（通常 120 = 1格）
                        clicks = abs(wheel_delta) // 120
                        
                        x = mouse.dwMousePosition.X
                        y = mouse.dwMousePosition.Y
                        
                        print(f"{symbol} {direction:8s} | "
                              f"增量={wheel_delta:5d} | "
                              f"格数={clicks} | "
                              f"位置=({x:3d},{y:3d}) | "
                              f"累计: ↑{wheel_up_count} ↓{wheel_down_count}")
                    
                    # 水平滚轮
                    elif mouse.dwEventFlags & MOUSE_HWHEELED:
                        wheel_delta = ctypes.c_short(mouse.dwButtonState >> 16).value
                        direction = "→ 向右" if wheel_delta > 0 else "← 向左"
                        
                        x = mouse.dwMousePosition.X
                        y = mouse.dwMousePosition.Y
                        
                        print(f"◆ {direction:8s} | "
                              f"增量={wheel_delta:5d} | "
                              f"位置=({x:3d},{y:3d})")
    
    except KeyboardInterrupt:
        print("\n\n中断")
    
    finally:
        kernel32.SetConsoleMode(h_stdin, old_mode)
        
        print("\n" + "=" * 70)
        print("滚轮统计:")
        print(f"  向上滚动: {wheel_up_count} 次")
        print(f"  向下滚动: {wheel_down_count} 次")
        print(f"  总增量: {total_delta}")
        print("=" * 70)

if __name__ == "__main__":
    main()
