import msvcrt
import sys

def read_key():
    """读取按键（Windows）"""
    if msvcrt.kbhit():
        # 读取第一个字节
        ch = msvcrt.getch()
        
        # 如果是特殊键前缀（0x00 或 0xe0），读取第二个字节
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            return ch + ch2
        
        return ch
    
    return None

# 测试
print("按方向键查看编码（按 q 退出）：")
print("=" * 60)

while True:
    key = read_key()
    
    if key:
        # 检查退出
        if key == b'q':
            print("\n退出")
            break
        
        # 显示编码
        print(f"\n原始字节: {key}")
        print(f"十六进制: {' '.join(f'{b:02X}' for b in key)}")
        print(f"十进制:   {' '.join(str(b) for b in key)}")
        print("-" * 60)
