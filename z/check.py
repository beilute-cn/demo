#!/usr/bin/env python3
"""
自动获取并解析终端设备属性
支持 Windows, Linux, macOS
"""

import sys
import os
import platform
import re
import threading
from typing import Optional, Dict
from io import StringIO

# 根据操作系统导入不同的模块
IS_WINDOWS = platform.system() == 'Windows'

if not IS_WINDOWS:
    import termios
    import tty
    import select
else:
    import msvcrt
    import time
    import ctypes
    from ctypes import wintypes


class WindowsConsole:
    """Windows 控制台处理"""
    
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    ENABLE_VIRTUAL_TERMINAL_INPUT = 0x0200
    
    @staticmethod
    def enable_ansi():
        """启用 ANSI 转义序列支持"""
        if not IS_WINDOWS:
            return True
        
        try:
            kernel32 = ctypes.windll.kernel32
            
            # 启用输出的虚拟终端处理
            h_out = kernel32.GetStdHandle(WindowsConsole.STD_OUTPUT_HANDLE)
            mode_out = wintypes.DWORD()
            kernel32.GetConsoleMode(h_out, ctypes.byref(mode_out))
            mode_out.value |= WindowsConsole.ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(h_out, mode_out)
            
            # 启用输入的虚拟终端处理
            h_in = kernel32.GetStdHandle(WindowsConsole.STD_INPUT_HANDLE)
            mode_in = wintypes.DWORD()
            kernel32.GetConsoleMode(h_in, ctypes.byref(mode_in))
            mode_in.value |= WindowsConsole.ENABLE_VIRTUAL_TERMINAL_INPUT
            kernel32.SetConsoleMode(h_in, mode_in)
            
            return True
        except Exception as e:
            print(f"警告: 无法启用 ANSI 支持: {e}", file=sys.stderr)
            return False


class TerminalAttributesParser:
    """终端属性解析器"""
    
    ATTRIBUTES_MAP = {
        1: "132 列模式",
        2: "打印机端口",
        3: "ReGIS 图形",
        4: "六倍速打印",
        6: "选择性擦除",
        7: "软字符集 (DRCS)",
        8: "用户定义键",
        9: "国家替换字符集",
        12: "南斯拉夫字符集",
        13: "塞尔维亚-克罗地亚字符集",
        14: "DEC 技术字符集",
        15: "技术字符集",
        16: "定位报告",
        17: "终端状态行",
        18: "用户窗口",
        19: "双向支持",
        21: "水平滚动",
        22: "ANSI 颜色/文本颜色",
        23: "希腊字符集",
        24: "土耳其字符集",
        28: "矩形区域操作",
        29: "文本宏",
        32: "文本定位",
        42: "ISO Latin-2 字符集",
        44: "PCTerm",
        45: "软键映射",
        46: "ASCII 仿真",
        52: "控制字符集",
        53: "希伯来字符集",
        61: "VT220 级别",
        62: "VT240 级别",
        63: "VT320 级别",
        64: "VT420 级别",
        65: "VT510 级别",
        66: "VT520 级别",
    }
    
    TERMINAL_TYPES = {
        1: "VT100",
        2: "VT100 with AVO",
        6: "VT102",
        61: "VT220",
        62: "VT240",
        63: "VT320",
        64: "VT420",
        65: "VT510",
    }
    
    @classmethod
    def parse(cls, response: str) -> Dict:
        """解析终端响应"""
        if not response:
            return {
                "raw_response": "",
                "has_private_marker": False,
                "terminal_type": "未知",
                "parameter_count": 0,
                "parameters": [],
                "attributes": []
            }
        
        # 移除 ESC 和 CSI 前缀
        content = response
        if content.startswith("\033[") or content.startswith("\x1b["):
            content = content[2:]
        elif content.startswith("^[["):
            content = content[3:]
        
        # 检查是否有私有标记
        has_private = content.startswith("?")
        if has_private:
            content = content[1:]
        
        # 移除终止符
        if content.endswith("c"):
            content = content[:-1]
        
        # 分割参数
        try:
            params = [int(x) for x in content.split(";") if x]
        except ValueError:
            params = []
        
        # 识别终端类型
        terminal_type = "未知"
        if params:
            terminal_type = cls.TERMINAL_TYPES.get(params[0], f"未知 (代码: {params[0]})")
        
        # 解析所有属性
        attributes = []
        for param in params:
            description = cls.ATTRIBUTES_MAP.get(param, f"未知属性")
            attributes.append({
                "code": param,
                "description": description
            })
        
        return {
            "raw_response": response,
            "has_private_marker": has_private,
            "terminal_type": terminal_type,
            "parameter_count": len(params),
            "parameters": params,
            "attributes": attributes
        }


class UnixTerminalQuery:
    """Unix/Linux/macOS 终端查询"""
    
    def __init__(self, timeout: float = 0.5):
        self.timeout = timeout
        self.old_settings = None
    
    def query(self, query_string: str) -> Optional[str]:
        """发送查询并获取响应"""
        if not sys.stdin.isatty():
            return None
        
        try:
            # 保存并设置终端为原始模式
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            
            # 发送查询
            sys.stdout.write(query_string)
            sys.stdout.flush()
            
            # 读取响应
            response = ""
            while True:
                ready, _, _ = select.select([sys.stdin], [], [], self.timeout)
                
                if ready:
                    char = sys.stdin.read(1)
                    response += char
                    
                    # 检查是否收到完整响应
                    if char == 'c' and ('\033[' in response or '\x1b[' in response):
                        break
                else:
                    # 超时
                    break
            
            return response if response else None
            
        except Exception as e:
            print(f"查询错误: {e}", file=sys.stderr)
            return None
        
        finally:
            # 恢复终端设置
            if self.old_settings:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)


class WindowsTerminalQuery:
    """Windows 终端查询（改进版）"""
    
    def __init__(self, timeout: float = 0.5):
        self.timeout = timeout
        self.response = None
        self.reading = False
    
    def _read_input(self):
        """在后台线程中读取输入"""
        response = ""
        start_time = time.time()
        
        while self.reading and (time.time() - start_time) < self.timeout:
            if msvcrt.kbhit():
                try:
                    # 读取一个字节
                    byte = msvcrt.getch()
                    
                    # 处理特殊字符
                    if byte == b'\x1b' or byte == b'\033':
                        response += '\x1b'
                    elif byte == b'\r':
                        continue
                    elif byte == b'\n':
                        continue
                    else:
                        try:
                            response += byte.decode('utf-8', errors='ignore')
                        except:
                            response += chr(byte[0]) if byte else ''
                    
                    # 检查是否收到完整响应
                    if 'c' in response and '\x1b[' in response:
                        break
                        
                except Exception as e:
                    pass
            else:
                time.sleep(0.001)  # 短暂休眠
        
        self.response = response if response else None
        self.reading = False
    
    def query(self, query_string: str) -> Optional[str]:
        """发送查询并获取响应"""
        
        # 发送查询
        sys.stdout.write(query_string)
        sys.stdout.flush()
        
        # 启动读取线程
        self.reading = True
        self.response = None
        
        reader_thread = threading.Thread(target=self._read_input, daemon=True)
        reader_thread.start()
        
        # 等待读取完成
        reader_thread.join(timeout=self.timeout + 0.1)
        self.reading = False
        
        return self.response


def get_terminal_query(timeout: float = 0.5):
    """根据操作系统获取相应的查询对象"""
    if IS_WINDOWS:
        return WindowsTerminalQuery(timeout=timeout)
    else:
        return UnixTerminalQuery(timeout=timeout)


def print_separator(char="=", length=70):
    """打印分隔线"""
    print(char * length)


def display_results(parsed_data: Dict):
    """显示解析结果"""
    
    print_separator()
    print("终端设备属性报告")
    print_separator()
    
    print(f"\n原始响应: {repr(parsed_data['raw_response'])}")
    print(f"终端类型: {parsed_data['terminal_type']}")
    print(f"私有标记: {'是' if parsed_data['has_private_marker'] else '否'}")
    print(f"参数数量: {parsed_data['parameter_count']}")
    
    if parsed_data['parameters']:
        print(f"\n参数列表: {parsed_data['parameters']}")
        
        print("\n支持的功能:")
        print_separator("-")
        
        for attr in parsed_data['attributes']:
            code = attr['code']
            desc = attr['description']
            print(f"  [{code:3d}] {desc}")
    
    print_separator()


def display_hex_dump(response: str):
    """显示十六进制转储"""
    if not response:
        return
    
    print("\n十六进制转储:")
    print_separator("-")
    
    for i, char in enumerate(response):
        byte_val = ord(char)
        hex_val = f"{byte_val:02x}"
        
        if byte_val < 32 or byte_val > 126:
            display_char = f"<{hex_val}>"
        else:
            display_char = char
        
        print(f"  位置 {i:2d}: 0x{hex_val} ({byte_val:3d}) '{display_char}'")


def get_system_info():
    """获取系统信息"""
    print("\n系统信息:")
    print_separator("-")
    print(f"  操作系统: {platform.system()}")
    print(f"  平台: {platform.platform()}")
    print(f"  Python 版本: {platform.python_version()}")
    print(f"  交互式终端: {'是' if sys.stdin.isatty() else '否'}")
    
    # 获取环境变量中的终端信息
    term = os.environ.get('TERM', '未设置')
    term_program = os.environ.get('TERM_PROGRAM', '未设置')
    wt_session = os.environ.get('WT_SESSION', '未设置')
    
    print(f"  TERM: {term}")
    print(f"  TERM_PROGRAM: {term_program}")
    
    if IS_WINDOWS:
        print(f"  WT_SESSION: {wt_session}")
        if wt_session != '未设置':
            print(f"  检测到: Windows Terminal")


def main():
    """主函数"""
    
    print("=" * 70)
    print("终端设备属性自动查询工具")
    print("=" * 70)
    
    # Windows 特殊处理
    if IS_WINDOWS:
        ansi_enabled = WindowsConsole.enable_ansi()
        print(f"\nANSI 支持: {'已启用' if ansi_enabled else '未启用'}")
    
    # 显示系统信息
    get_system_info()
    
    # 创建查询对象
    print("\n" + "=" * 70)
    print("正在查询主设备属性 (DA1)...")
    print("=" * 70)
    
    query = get_terminal_query(timeout=0.5)
    
    # 查询主设备属性
    response = query.query("\033[c")
    
    if response:
        print(f"\n✓ 成功收到响应 (长度: {len(response)} 字节)")
        
        # 解析响应
        parsed = TerminalAttributesParser.parse(response)
        
        # 显示结果
        display_results(parsed)
        
        # 显示十六进制转储
        display_hex_dump(response)
        
    else:
        print("\n✗ 未收到响应或超时")
        print("\n可能的原因:")
        print("  1. 终端不支持设备属性查询")
        print("  2. 响应超时（尝试增加超时时间）")
        print("  3. 不在交互式终端中运行")
        
        if IS_WINDOWS:
            print("\nWindows 用户建议:")
            print("  - 使用 Windows Terminal (推荐)")
            print("  - 确保使用最新版本的终端")
            print("  - 某些旧版 CMD 可能不支持")
    
    # 查询次设备属性 (DA2)
    print("\n" + "=" * 70)
    print("正在查询次设备属性 (DA2)...")
    print("=" * 70)
    
    response2 = query.query("\033[>c")
    
    if response2:
        print(f"\n✓ 收到响应: {repr(response2)}")
        
        # 解析 DA2 响应 (格式: ESC[>Pp;Pv;Pc)
        match = re.search(r'\x1b\[>(\d+);(\d+);(\d+)c', response2)
        if match:
            terminal_id = match.group(1)
            firmware_version = match.group(2)
            keyboard_type = match.group(3)
            
            print(f"\n次设备属性:")
            print_separator("-")
            print(f"  终端 ID: {terminal_id}")
            print(f"  固件版本: {firmware_version}")
            print(f"  键盘类型: {keyboard_type}")
            print_separator()
    else:
        print("\n✗ 未收到 DA2 响应")
    
    print("\n" + "=" * 70)
    print("查询完成")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
