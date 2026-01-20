import msvcrt
import os

class WindowsKeyTester:
    """Windows 按键测试工具"""
    
    def __init__(self):
        self.mode = 'normal'
    
    def clear_screen(self):
        """清屏"""
        os.system('cls')
    
    def show_menu(self):
        """显示菜单"""
        self.clear_screen()
        print("=" * 70)
        print("Windows 按键编码测试工具")
        print("=" * 70)
        print("\n命令:")
        print("  1 - 简单模式（只显示按键名称）")
        print("  2 - 详细模式（显示完整编码）")
        print("  h - 显示帮助")
        print("  q - 退出")
        print("\n当前模式:", "详细模式" if self.mode == 'detail' else "简单模式")
        print("=" * 70)
        print("\n按任意键开始...")
    
    def run(self):
        """运行测试"""
        self.show_menu()
        
        while True:
            if msvcrt.kbhit():
                key = self.read_key()
                
                if key == b'q':
                    print("\n退出")
                    break
                elif key == b'1':
                    self.mode = 'normal'
                    self.show_menu()
                elif key == b'2':
                    self.mode = 'detail'
                    self.show_menu()
                elif key == b'h':
                    self.show_menu()
                else:
                    self.display_key(key)
    
    def read_key(self):
        """读取按键"""
        ch = msvcrt.getch()
        
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            return ch + ch2
        
        return ch
    
    def display_key(self, key):
        """显示按键信息"""
        if self.mode == 'normal':
            name = self.identify_key(key)
            print(f"按键: {name}")
        else:
            print("\n" + "-" * 70)
            name = self.identify_key(key)
            hex_str = ' '.join(f'{b:02X}' for b in key)
            dec_str = ' '.join(f'{b:3d}' for b in key)
            
            print(f"按键名称: {name}")
            print(f"十六进制: {hex_str}")
            print(f"十进制:   {dec_str}")
            print(f"字节数:   {len(key)}")
            print("-" * 70)
    
    def identify_key(self, key):
        """识别按键"""
        keys = {
            b'\xe0H': '↑ UP',
            b'\xe0P': '↓ DOWN',
            b'\xe0M': '→ RIGHT',
            b'\xe0K': '← LEFT',
            b'\xe0G': 'HOME',
            b'\xe0O': 'END',
            b'\xe0R': 'INSERT',
            b'\xe0S': 'DELETE',
            b'\xe0I': 'PAGE UP',
            b'\xe0Q': 'PAGE DOWN',
            b'\x00;': 'F1',
            b'\x00<': 'F2',
            b'\x00=': 'F3',
            b'\x00>': 'F4',
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
                return f"字符 '{decoded}'"
        except:
            pass
        
        return "未知按键"

# 运行
if __name__ == '__main__':
    tester = WindowsKeyTester()
    tester.run()
