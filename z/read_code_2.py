import msvcrt
import sys

class WindowsKeyReader:
    """Windows 按键编码读取器"""
    
    # Windows 方向键编码
    ARROW_KEYS = {
        b'\xe0H': '↑ UP',
        b'\xe0P': '↓ DOWN',
        b'\xe0M': '→ RIGHT',
        b'\xe0K': '← LEFT',
        b'\x00H': '↑ UP (备用)',
        b'\x00P': '↓ DOWN (备用)',
        b'\x00M': '→ RIGHT (备用)',
        b'\x00K': '← LEFT (备用)',
    }
    
    # 其他特殊键
    SPECIAL_KEYS = {
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
        b'\x00?': 'F5',
        b'\x00@': 'F6',
        b'\x00A': 'F7',
        b'\x00B': 'F8',
        b'\x00C': 'F9',
        b'\x00D': 'F10',
        b'\x08': 'BACKSPACE',
        b'\r': 'ENTER',
        b'\t': 'TAB',
        b'\x1b': 'ESC',
        b'\x03': 'Ctrl+C',
        b' ': 'SPACE',
    }
    
    def read_key(self):
        """读取按键"""
        if not msvcrt.kbhit():
            return None
        
        # 读取第一个字节
        ch = msvcrt.getch()
        
        # 检查是否是特殊键前缀
        if ch in (b'\x00', b'\xe0'):
            # 读取第二个字节
            ch2 = msvcrt.getch()
            return ch + ch2
        
        return ch
    
    def get_key_info(self, key):
        """获取按键详细信息"""
        if key is None:
            return None
        
        return {
            'raw': key,
            'hex': [f'{b:02X}' for b in key],
            'dec': [b for b in key],
            'oct': [f'{b:03o}' for b in key],
            'length': len(key),
            'name': self.identify_key(key),
        }
    
    def identify_key(self, key):
        """识别按键名称"""
        # 检查方向键
        if key in self.ARROW_KEYS:
            return self.ARROW_KEYS[key]
        
        # 检查其他特殊键
        if key in self.SPECIAL_KEYS:
            return self.SPECIAL_KEYS[key]
        
        # 普通字符
        try:
            decoded = key.decode('utf-8', errors='ignore')
            if decoded.isprintable():
                return f"字符 '{decoded}'"
        except:
            pass
        
        return "未知按键"
    
    def display_key_info(self, info):
        """显示按键信息"""
        if info is None:
            return
        
        print("\n" + "=" * 70)
        print(f"按键名称: {info['name']}")
        print("=" * 70)
        print(f"原始字节: {info['raw']}")
        print(f"十六进制: {' '.join(info['hex'])}")
        print(f"十进制:   {' '.join(map(str, info['dec']))}")
        print(f"八进制:   {' '.join(info['oct'])}")
        print(f"字节数:   {info['length']}")
        
        # 详细分析
        print("\n详细分析:")
        for i, (byte, hex_val) in enumerate(zip(info['dec'], info['hex'])):
            char_name = self.get_char_name(byte)
            print(f"  字节 {i+1}: 0x{hex_val} ({byte:3d}) - {char_name}")
        
        print("=" * 70)
    
    @staticmethod
    def get_char_name(byte_val):
        """获取字符名称"""
        names = {
            0x00: '0x00 (特殊键前缀 1)',
            0xe0: '0xE0 (特殊键前缀 2)',
            0x48: 'H (UP)',
            0x50: 'P (DOWN)',
            0x4d: 'M (RIGHT)',
            0x4b: 'K (LEFT)',
            0x47: 'G (HOME)',
            0x4f: 'O (END)',
            0x52: 'R (INSERT)',
            0x53: 'S (DELETE)',
            0x49: 'I (PAGE UP)',
            0x51: 'Q (PAGE DOWN)',
            0x08: 'BACKSPACE',
            0x0d: 'ENTER',
            0x09: 'TAB',
            0x1b: 'ESC',
            0x20: 'SPACE',
        }
        
        if byte_val in names:
            return names[byte_val]
        elif 32 <= byte_val <= 126:
            return f"'{chr(byte_val)}'"
        else:
            return '控制字符'

# 使用示例
if __name__ == '__main__':
    print("Windows 按键编码读取器")
    print("按任意键查看编码（按 Ctrl+C 退出）")
    
    reader = WindowsKeyReader()
    
    while True:
        key = reader.read_key()
        
        if key:
            info = reader.get_key_info(key)
            
            # Ctrl+C 退出
            if key == b'\x03':
                print("\n退出")
                break
            
            reader.display_key_info(info)
