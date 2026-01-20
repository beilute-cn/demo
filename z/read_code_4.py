import msvcrt
import time
from datetime import datetime

class RealtimeMonitor:
    """实时按键监控器"""
    
    def __init__(self):
        self.running = False
    
    def monitor(self):
        """开始监控"""
        print("实时按键监控器（Windows）")
        print("=" * 80)
        print(f"{'时间':<12} | {'十六进制':<20} | {'十进制':<15} | {'按键'}")
        print("-" * 80)
        
        self.running = True
        
        while self.running:
            if msvcrt.kbhit():
                # 读取按键
                ch = msvcrt.getch()
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                
                # 检查特殊键
                if ch in (b'\x00', b'\xe0'):
                    ch2 = msvcrt.getch()
                    key = ch + ch2
                else:
                    key = ch
                
                # Ctrl+C 退出
                if key == b'\x03':
                    print("\n退出监控")
                    break
                
                # 显示信息
                hex_str = ' '.join(f'{b:02X}' for b in key)
                dec_str = ' '.join(f'{b:3d}' for b in key)
                name = self.identify_key(key)
                
                print(f"{timestamp:<12} | {hex_str:<20} | {dec_str:<15} | {name}")
    
    def identify_key(self, key):
        """识别按键"""
        keys = {
            b'\xe0H': '↑ UP',
            b'\xe0P': '↓ DOWN',
            b'\xe0M': '→ RIGHT',
            b'\xe0K': '← LEFT',
            b'\r': 'ENTER',
            b'\x08': 'BACKSPACE',
            b'\t': 'TAB',
            b'\x1b': 'ESC',
            b' ': 'SPACE',
        }
        
        if key in keys:
            return keys[key]
        
        try:
            decoded = key.decode('utf-8', errors='ignore')
            if decoded.isprintable():
                return f"'{decoded}'"
        except:
            pass
        
        return "未知"

# 使用
if __name__ == '__main__':
    monitor = RealtimeMonitor()
    monitor.monitor()
