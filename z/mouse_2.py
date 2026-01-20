import ctypes
from ctypes import wintypes
import time

# Windows API 常量
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_WINDOW_INPUT = 0x0008
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

# 事件类型
KEY_EVENT = 0x0001
MOUSE_EVENT = 0x0002

# 鼠标按钮
FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001
RIGHTMOST_BUTTON_PRESSED = 0x0002
FROM_LEFT_2ND_BUTTON_PRESSED = 0x0004

# 鼠标事件标志
MOUSE_MOVED = 0x0001
DOUBLE_CLICK = 0x0002
MOUSE_WHEELED = 0x0004
MOUSE_HWHEELED = 0x0008

# 结构体
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
    
    # 保存旧模式
    old_mode = wintypes.DWORD()
    kernel32.GetConsoleMode(h_stdin, ctypes.byref(old_mode))
    
    # 启用鼠标输入
    new_mode = ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS | ENABLE_WINDOW_INPUT
    kernel32.SetConsoleMode(h_stdin, new_mode)
    
    # 启用 ANSI
    out_mode = wintypes.DWORD()
    kernel32.GetConsoleMode(h_stdout, ctypes.byref(out_mode))
    kernel32.SetConsoleMode(h_stdout, out_mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    
    print("\033[2J\033[H")  # 清屏
    print("=" * 70)
    print(" " * 15 + "完整鼠标事件监听（含滚轮）")
    print("=" * 70)
    print("\n支持的事件:")
    print("  • 左键/右键/中键 点击")
    print("  • 鼠标移动")
    print("  • 垂直滚轮（上/下）")
    print("  • 水平滚轮（左/右）")
    print("  • 双击")
    print("\n按 'q' 退出\n")
    
    input_record = INPUT_RECORD()
    events_read = wintypes.DWORD()
    event_count = 0
    last_button_state = 0
    
    # 统计
    stats = {
        '左键': 0,
        '右键': 0,
        '中键': 0,
        '滚轮上': 0,
        '滚轮下': 0,
        '水平滚轮': 0,
        '移动': 0,
        '双击': 0
    }
    
    try:
        while True:
            # 检查事件数量
            num_events = wintypes.DWORD()
            kernel32.GetNumberOfConsoleInputEvents(h_stdin, ctypes.byref(num_events))
            
            if num_events.value == 0:
                time.sleep(0.01)
                continue
            
            # 读取事件
            if kernel32.ReadConsoleInputW(h_stdin, ctypes.byref(input_record), 1, ctypes.byref(events_read)):
                if events_read.value == 0:
                    continue
                
                # 检测退出键
                if input_record.EventType == KEY_EVENT:
                    key = input_record.Event.KeyEvent
                    if key.bKeyDown and key.uChar.lower() == 'q':
                        break
                
                # 处理鼠标事件
                if input_record.EventType == MOUSE_EVENT:
                    mouse = input_record.Event.MouseEvent
                    x = mouse.dwMousePosition.X
                    y = mouse.dwMousePosition.Y
                    state = mouse.dwButtonState
                    flags = mouse.dwEventFlags
                    
                    event_info = None
                    
                    # 1. 垂直滚轮事件（最重要！）
                    if flags & MOUSE_WHEELED:
                        # 滚轮增量在高16位
                        wheel_delta = ctypes.c_short(state >> 16).value
                        
                        # WHEEL_DELTA = 120，正值向上，负值向下
                        direction = "上" if wheel_delta > 0 else "下"
                        clicks = abs(wheel_delta) // 120  # 滚动格数
                        
                        event_count += 1
                        event_info = f"滚轮{direction:2s}"
                        stats[f'滚轮{direction}'] += 1
                        
                        print(f"[{event_count:4d}] {event_info:12s} "
                              f"增量={wheel_delta:5d} 格数={clicks} "
                              f"位置=({x:3d},{y:3d})")
                    
                    # 2. 水平滚轮事件
                    elif flags & MOUSE_HWHEELED:
                        wheel_delta = ctypes.c_short(state >> 16).value
                        direction = "右" if wheel_delta > 0 else "左"
                        
                        event_count += 1
                        event_info = f"水平滚轮{direction}"
                        stats['水平滚轮'] += 1
                        
                        print(f"[{event_count:4d}] {event_info:12s} "
                              f"增量={wheel_delta:5d} "
                              f"位置=({x:3d},{y:3d})")
                    
                    # 3. 双击事件
                    elif flags & DOUBLE_CLICK:
                        event_count += 1
                        event_info = "双击"
                        stats['双击'] += 1
                        
                        buttons = []
                        if state & FROM_LEFT_1ST_BUTTON_PRESSED:
                            buttons.append("左键")
                        if state & RIGHTMOST_BUTTON_PRESSED:
                            buttons.append("右键")
                        if state & FROM_LEFT_2ND_BUTTON_PRESSED:
                            buttons.append("中键")
                        
                        button_str = "+".join(buttons) if buttons else "未知"
                        
                        print(f"[{event_count:4d}] {event_info:12s} "
                              f"按钮={button_str:8s} "
                              f"位置=({x:3d},{y:3d})")
                    
                    # 4. 移动事件
                    elif flags & MOUSE_MOVED:
                        # 移动事件太多，只在有按钮按下时显示（拖动）
                        if state != 0:
                            event_count += 1
                            event_info = "拖动"
                            stats['移动'] += 1
                            
                            buttons = []
                            if state & FROM_LEFT_1ST_BUTTON_PRESSED:
                                buttons.append("左键")
                            if state & RIGHTMOST_BUTTON_PRESSED:
                                buttons.append("右键")
                            if state & FROM_LEFT_2ND_BUTTON_PRESSED:
                                buttons.append("中键")
                            
                            button_str = "+".join(buttons)
                            
                            print(f"[{event_count:4d}] {event_info:12s} "
                                  f"按钮={button_str:8s} "
                                  f"位置=({x:3d},{y:3d})")
                    
                    # 5. 按钮状态变化（点击/释放）
                    elif state != last_button_state:
                        event_count += 1
                        
                        # 判断是按下还是释放
                        if state > last_button_state:
                            action = "按下"
                            # 找出哪个按钮被按下
                            diff = state & ~last_button_state
                        else:
                            action = "释放"
                            diff = last_button_state & ~state
                        
                        button = ""
                        if diff & FROM_LEFT_1ST_BUTTON_PRESSED:
                            button = "左键"
                            if action == "按下":
                                stats['左键'] += 1
                        elif diff & RIGHTMOST_BUTTON_PRESSED:
                            button = "右键"
                            if action == "按下":
                                stats['右键'] += 1
                        elif diff & FROM_LEFT_2ND_BUTTON_PRESSED:
                            button = "中键"
                            if action == "按下":
                                stats['中键'] += 1
                        
                        if button:
                            event_info = f"{action}{button}"
                            print(f"[{event_count:4d}] {event_info:12s} "
                                  f"位置=({x:3d},{y:3d})")
                        
                        last_button_state = state
    
    except KeyboardInterrupt:
        print("\n\n程序中断")
    
    finally:
        # 恢复模式
        kernel32.SetConsoleMode(h_stdin, old_mode)
        
        # 显示统计
        print("\n" + "=" * 70)
        print(" " * 25 + "事件统计")
        print("=" * 70)
        print(f"总事件数: {event_count}")
        print("\n详细统计:")
        for event_type, count in stats.items():
            if count > 0:
                print(f"  {event_type:12s}: {count:4d} 次")
        print("=" * 70)

if __name__ == "__main__":
    main()
