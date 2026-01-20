import msvcrt

def get_arrow_key():
    """获取方向键"""
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        
        # 特殊键
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            
            # 方向键映射
            arrows = {
                b'H': 'UP',
                b'P': 'DOWN',
                b'M': 'RIGHT',
                b'K': 'LEFT',
            }
            
            return arrows.get(ch2, None)
        
        # Ctrl+C
        if ch == b'\x03':
            return 'EXIT'
        
        # 其他键
        try:
            return ch.decode('utf-8')
        except:
            return None
    
    return None

# 测试
print("按方向键测试（按 Ctrl+C 退出）：")

while True:
    key = get_arrow_key()
    
    if key == 'EXIT':
        print("\n退出")
        break
    
    if key:
        if key == 'UP':
            print("↑ 向上")
        elif key == 'DOWN':
            print("↓ 向下")
        elif key == 'LEFT':
            print("← 向左")
        elif key == 'RIGHT':
            print("→ 向右")
        else:
            print(f"其他键: {key}")
