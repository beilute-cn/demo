import sys
import platform

# 根据系统导入不同模块
if platform.system() == 'Windows':
    import msvcrt
else:
    import tty
    import termios
    import select

class CrossPlatformKeyReader:
    """跨平台按键读取器"""
    
    def __init__(self):
        self.is_windows = platform.system() == 'Windows'
        if not self.is_windows:
            self.fd = sys.stdin.fileno()
            self.old_settings = None
    
    def __enter__(self):
        if not self.is_windows:
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setraw(self.fd)
        return self
    
    def __exit__(self, *args):
        if not self.is_windows and self.old_settings:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
    
    def read_key(self):
        """读取按键"""
        if self.is_windows:
            return self._read_key_windows()
        else:
            return self._read_key_unix()
    
    def _read_key_windows(self):
        """Windows 读取"""
        if not msvcrt.kbhit():
            return None
        
        ch = msvcrt.getch()
        
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            return ch + ch2
        
        return ch
    
    def _read_key_unix(self):
        """Unix/Linux/Mac 读取"""
        chars = [sys.stdin.read(1)]
        
        if chars[0] == '\x1b':
            while select.select([sys.stdin], [], [], 0.1)[0]:
                chars.append(sys.stdin.read(1))
        
        return ''.join(chars).encode('latin1')
    
    def identify_key(self, key):
        """识别按键"""
        if key is None:
            return None
        
        # Windows 编码
        windows_keys = {
            b'\xe0H': 'UP',
            b'\xe0P': 'DOWN',
            b'\xe0M': 'RIGHT',
            b'\xe0K': 'LEFT',
        }
        
        # Unix 编码
        unix_keys = {
            b'\x1b[A': 'UP',
            b'\x1b[B': 'DOWN',
            b'\x1b[C': 'RIGHT',
            b'\x1b[D': 'LEFT',
        }
        
        # 检查
        if key in windows_keys:
            return windows_keys[key]
        if key in unix_keys:
            return unix_keys[key]
        
        # Ctrl+C
        if key == b'\x03':
            return 'EXIT'
        
        return None

# 使用示例
if __name__ == '__main__':
    print(f"跨平台按键读取器（当前系统: {platform.system()}）")
    print("按方向键测试（按 Ctrl+C 退出）：")
    
    with CrossPlatformKeyReader() as reader:
        while True:
            key = reader.read_key()
            
            if key:
                name = reader.identify_key(key)
                
                if name == 'EXIT':
                    print("\n退出")
                    break
                
                if name:
                    arrows = {
                        'UP': '↑ 向上',
                        'DOWN': '↓ 向下',
                        'LEFT': '← 向左',
                        'RIGHT': '→ 向右',
                    }
                    print(arrows.get(name, name))
                    
                    # 显示编码
                    hex_str = ' '.join(f'{b:02X}' for b in key)
                    print(f"  编码: {hex_str}")
