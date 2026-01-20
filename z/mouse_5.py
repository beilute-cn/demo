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

class MouseTracker:
    def __init__(self, show_move=False, drag_threshold=0):
        self.kernel32 = ctypes.windll.kernel32
        self.h_stdin = self.kernel32.GetStdHandle(STD_INPUT_HANDLE)
        self.h_stdout = self.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        self.old_mode = wintypes.DWORD()
        
        self.event_count = 0
        self.last_button_state = 0
        self.is_dragging = False  # 是否正在拖动
        self.drag_start_pos = None  # 拖动起始位置
        self.show_move = show_move  # 是否显示普通移动
        self.drag_threshold = drag_threshold  # 拖动阈值（像素）
        
        # 统计
        self.stats = {
            '左键': 0,
            '右键': 0,
            '中键': 0,
            '滚轮上': 0,
            '滚轮下': 0,
            '拖动': 0,
            '移动': 0,
            '双击': 0
        }
    
    def setup(self):
        """设置控制台模式"""
        self.kernel32.GetConsoleMode(self.h_stdin, ctypes.byref(self.old_mode))
        new_mode = ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS | ENABLE_WINDOW_INPUT
        self.kernel32.SetConsoleMode(self.h_stdin, new_mode)
        
        out_mode = wintypes.DWORD()
        self.kernel32.GetConsoleMode(self.h_stdout, ctypes.byref(out_mode))
        self.kernel32.SetConsoleMode(self.h_stdout, out_mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
    
    def restore(self):
        """恢复控制台模式"""
        self.kernel32.SetConsoleMode(self.h_stdin, self.old_mode)
    
    def get_button_name(self, state):
        """获取按钮名称"""
        buttons = []
        if state & FROM_LEFT_1ST_BUTTON_PRESSED:
            buttons.append("左键")
        if state & RIGHTMOST_BUTTON_PRESSED:
            buttons.append("右键")
        if state & FROM_LEFT_2ND_BUTTON_PRESSED:
            buttons.append("中键")
        return "+".join(buttons) if buttons else ""
    
    def handle_mouse_event(self, mouse):
        """处理鼠标事件"""
        x = mouse.dwMousePosition.X
        y = mouse.dwMousePosition.Y
        state = mouse.dwButtonState
        flags = mouse.dwEventFlags
        
        # 1. 滚轮事件（优先级最高）
        if flags & MOUSE_WHEELED:
            wheel_delta = ctypes.c_short(state >> 16).value
            direction = "上" if wheel_delta > 0 else "下"
            clicks = abs(wheel_delta) // 120
            
            self.event_count += 1
            self.stats[f'滚轮{direction}'] += 1
            
            print(f"[{self.event_count:4d}] 滚轮{direction:2s}      "
                  f"增量={wheel_delta:5d} 格数={clicks} "
                  f"位置=({x:3d},{y:3d})")
            return
        
        if flags & MOUSE_HWHEELED:
            wheel_delta = ctypes.c_short(state >> 16).value
            direction = "右" if wheel_delta > 0 else "左"
            
            self.event_count += 1
            
            print(f"[{self.event_count:4d}] 水平滚轮{direction}  "
                  f"增量={wheel_delta:5d} "
                  f"位置=({x:3d},{y:3d})")
            return
        
        # 2. 双击事件
        if flags & DOUBLE_CLICK:
            button_name = self.get_button_name(state)
            
            self.event_count += 1
            self.stats['双击'] += 1
            
            print(f"[{self.event_count:4d}] 双击        "
                  f"按钮={button_name:8s} "
                  f"位置=({x:3d},{y:3d})")
            return
        
        # 3. 移动事件
        if flags & MOUSE_MOVED:
            # 检查是否有按钮按下（拖动）
            if state != 0:
                # 有按钮按下 = 拖动
                if not self.is_dragging:
                    # 开始拖动
                    self.is_dragging = True
                    self.drag_start_pos = (x, y)
                
                # 检查是否超过阈值
                if self.drag_start_pos:
                    dx = abs(x - self.drag_start_pos[0])
                    dy = abs(y - self.drag_start_pos[1])
                    
                    if dx >= self.drag_threshold or dy >= self.drag_threshold:
                        button_name = self.get_button_name(state)
                        
                        self.event_count += 1
                        self.stats['拖动'] += 1
                        
                        print(f"[{self.event_count:4d}] 拖动        "
                              f"按钮={button_name:8s} "
                              f"位置=({x:3d},{y:3d})")
            else:
                # 没有按钮按下 = 普通移动
                self.is_dragging = False
                self.drag_start_pos = None
                
                if self.show_move:
                    self.event_count += 1
                    self.stats['移动'] += 1
                    
                    print(f"[{self.event_count:4d}] 移动        "
                          f"位置=({x:3d},{y:3d})")
            return
        
        # 4. 按钮状态变化（点击/释放）
        if state != self.last_button_state:
            # 判断是按下还是释放
            if state > self.last_button_state:
                action = "按下"
                diff = state & ~self.last_button_state
            else:
                action = "释放"
                diff = self.last_button_state & ~state
                # 释放时结束拖动
                self.is_dragging = False
                self.drag_start_pos = None
            
            # 找出哪个按钮
            button = ""
            if diff & FROM_LEFT_1ST_BUTTON_PRESSED:
                button = "左键"
                if action == "按下":
                    self.stats['左键'] += 1
            elif diff & RIGHTMOST_BUTTON_PRESSED:
                button = "右键"
                if action == "按下":
                    self.stats['右键'] += 1
            elif diff & FROM_LEFT_2ND_BUTTON_PRESSED:
                button = "中键"
                if action == "按下":
                    self.stats['中键'] += 1
            
            if button:
                self.event_count += 1
                
                print(f"[{self.event_count:4d}] {action}{button:4s}    "
                      f"位置=({x:3d},{y:3d})")
            
            self.last_button_state = state
    
    def run(self):
        """运行主循环"""
        print("\033[2J\033[H")  # 清屏
        print("=" * 70)
        print(" " * 20 + "鼠标事件监听器")
        print("=" * 70)
        print(f"\n配置:")
        print(f"  • 显示普通移动: {'是' if self.show_move else '否'}")
        print(f"  • 拖动阈值: {self.drag_threshold} 像素")
        print(f"\n支持的事件:")
        print(f"  • 点击（左键/右键/中键）")
        print(f"  • 拖动（按住按钮移动）")
        print(f"  • 滚轮（上/下）")
        print(f"  • 双击")
        if self.show_move:
            print(f"  • 移动（无按钮）")
        print(f"\n按 'q' 退出\n")
        
        input_record = INPUT_RECORD()
        events_read = wintypes.DWORD()
        
        try:
            while True:
                num_events = wintypes.DWORD()
                self.kernel32.GetNumberOfConsoleInputEvents(
                    self.h_stdin, 
                    ctypes.byref(num_events)
                )
                
                if num_events.value == 0:
                    time.sleep(0.01)
                    continue
                
                if self.kernel32.ReadConsoleInputW(
                    self.h_stdin,
                    ctypes.byref(input_record),
                    1,
                    ctypes.byref(events_read)
                ):
                    if events_read.value == 0:
                        continue
                    
                    # 检测退出键
                    if input_record.EventType == KEY_EVENT:
                        key = input_record.Event.KeyEvent
                        if key.bKeyDown and key.uChar.lower() == 'q':
                            break
                    
                    # 处理鼠标事件
                    elif input_record.EventType == MOUSE_EVENT:
                        self.handle_mouse_event(input_record.Event.MouseEvent)
        
        except KeyboardInterrupt:
            print("\n\n程序中断")
        
        finally:
            self.show_stats()
    
    def show_stats(self):
        """显示统计信息"""
        print("\n" + "=" * 70)
        print(" " * 25 + "事件统计")
        print("=" * 70)
        print(f"总事件数: {self.event_count}")
        print("\n详细统计:")
        for event_type, count in self.stats.items():
            if count > 0:
                print(f"  {event_type:12s}: {count:4d} 次")
        print("=" * 70)

def main():
    import sys
    
    print("鼠标事件监听器配置\n")
    
    # 配置选项
    print("1. 是否显示普通移动事件（无按钮按下）？")
    print("   注意: 移动事件非常频繁，建议选择 '否'")
    choice = input("   (y/n, 默认 n): ").strip().lower()
    show_move = (choice == 'y')
    
    print("\n2. 拖动事件阈值（像素）")
    print("   设置为 0 = 显示所有拖动移动")
    print("   设置为 5 = 移动超过 5 像素才显示")
    try:
        threshold = int(input("   (默认 0): ").strip() or "0")
    except:
        threshold = 0
    
    print("\n正在启动...\n")
    time.sleep(1)
    
    tracker = MouseTracker(show_move=show_move, drag_threshold=threshold)
    tracker.setup()
    
    try:
        tracker.run()
    finally:
        tracker.restore()

if __name__ == "__main__":
    main()
