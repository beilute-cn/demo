import ctypes
from ctypes import wintypes
from parse import parse
from control import control
from tab import tab


class u_char(ctypes.Union):
    _fields_ = [
        ("unicode_char", wintypes.WCHAR),
        ("ascii_char", wintypes.CHAR),
    ]


class key_event_record(parse, ctypes.Structure):
    _fields_ = [
        ("b_key_down", wintypes.BOOL),
        ("w_repeat_count", wintypes.WORD),
        ("w_virtual_key_code", wintypes.WORD),
        ("w_virtual_scan_code", wintypes.WORD),
        ("u_char", u_char),
        ("dw_control_key_state", wintypes.DWORD),
    ]

    def parse(self):
        """
        print("格式: \\033[M<btn><x><y>")
        print()
        print("组成部分:")
        print("  \\033    = ESC 字符 (0x1B, 27)")
        print("  [       = 左方括号 (0x5B, 91)")
        print("  M       = 字母 M (0x4D, 77)")
        print("  <btn>   = 按钮码 + 32 (单字节 ASCII 字符)")
        print("  <x>     = X 坐标 + 32 (单字节 ASCII 字符)")
        print("  <y>     = Y 坐标 + 32 (单字节 ASCII 字符)")
        """

        # TODO \033[M<btn><x><y> 格式的鼠标事件解析

        user32 = ctypes.windll.user32
        # 获取按键名称
        buffer_anscii = ctypes.create_string_buffer(20)
        ctypes.memset(ctypes.addressof(buffer_anscii), 0, ctypes.sizeof(buffer_anscii))
        if user32.GetKeyNameTextA(self.w_virtual_scan_code << 16, buffer_anscii, 20):

            print(
                f""
                + f"<"
                + (f"\033[0m" if self.b_key_down else "\033[90m")
                + f"{buffer_anscii.value.decode('utf-8', errors='ignore')}"
                + " \033[32m"
                + f"{control(self.dw_control_key_state)}"
                + f"\033[0m>"
            )
        else:
            print(f"无按键名称")
            exit(-1)

    def __str__(self):
        # return f"{"↓" if self.b_key_down else "↑"}, {self.w_virtual_key_code}, {self.w_virtual_scan_code}, {self.u_char.ascii_char.decode('utf-8', errors='ignore')}<{self.u_char.ascii_char.hex()}>, {control_key(self.dw_control_key_state)}"
        return f"""\
{tab}按键：{"按下" if self.b_key_down else "释放"}
{tab}重复次数：{self.w_repeat_count}
{tab}虚拟键码：{self.w_virtual_key_code}
{tab}扫描码：{self.w_virtual_scan_code}
{tab}字符：{self.u_char.ascii_char.decode('utf-8', errors='ignore')}<{self.u_char.ascii_char.hex()}>
{tab}控制键状态：{control(self.dw_control_key_state)}\
"""

        return f"""\
{tab}b_key_down={self.b_key_down}
{tab}wVirtuw_repeat_countalKeyCode={self.w_repeat_count}
{tab}w_virtual_key_code={self.w_virtual_key_code})
{tab}w_virtual_scan_code={self.w_virtual_scan_code}
{tab}u_char={self.u_char.ascii_char}
{tab}dw_control_key_state={self.dw_control_key_state}\
"""
