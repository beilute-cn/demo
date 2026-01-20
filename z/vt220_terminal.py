#!/usr/bin/env python3
"""
VT220 终端模拟和属性解析
详细说明 VT220 终端的特性和功能
"""

import sys
import os
import platform
from typing import Dict, List, Optional

# 根据操作系统导入
IS_WINDOWS = platform.system() == "Windows"

if not IS_WINDOWS:
    import termios
    import tty
    import select
else:
    import msvcrt
    import time
    import ctypes
    from ctypes import wintypes


class VT220Terminal:
    """VT220 终端规范和功能"""

    # VT220 标准设备属性响应
    STANDARD_DA1_RESPONSE = "\033[?62;1;2;6;7;8;9c"

    # VT220 的特性代码
    VT220_ATTRIBUTES = {
        62: {
            "name": "VT220 级别",
            "description": "表示终端符合 VT220 标准",
            "category": "终端类型",
        },
        1: {
            "name": "132 列模式",
            "description": "支持 132 列显示模式（标准为 80 列）",
            "category": "显示功能",
        },
        2: {
            "name": "打印机端口",
            "description": "支持连接打印机",
            "category": "外设支持",
        },
        4: {
            "name": "六倍速打印",
            "description": "支持高速打印功能",
            "category": "打印功能",
        },
        6: {
            "name": "选择性擦除",
            "description": "支持选择性擦除屏幕内容",
            "category": "编辑功能",
        },
        7: {
            "name": "软字符集 (DRCS)",
            "description": "可下载可重定义字符集",
            "category": "字符集",
        },
        8: {
            "name": "用户定义键",
            "description": "支持用户自定义功能键",
            "category": "键盘功能",
        },
        9: {
            "name": "国家替换字符集",
            "description": "支持多国语言字符集",
            "category": "字符集",
        },
        15: {
            "name": "技术字符集",
            "description": "支持技术符号和特殊字符",
            "category": "字符集",
        },
        18: {
            "name": "用户窗口",
            "description": "支持用户定义的窗口区域",
            "category": "显示功能",
        },
        21: {
            "name": "水平滚动",
            "description": "支持水平方向滚动",
            "category": "滚动功能",
        },
        22: {
            "name": "ANSI 颜色",
            "description": "支持 ANSI 颜色显示",
            "category": "显示功能",
        },
        23: {
            "name": "希腊字符集",
            "description": "支持希腊语字符",
            "category": "字符集",
        },
    }

    # VT220 支持的控制序列
    CONTROL_SEQUENCES = {
        "光标控制": {
            "\033[H": "光标移到左上角",
            "\033[{row};{col}H": "光标移到指定位置",
            "\033[A": "光标上移一行",
            "\033[B": "光标下移一行",
            "\033[C": "光标右移一列",
            "\033[D": "光标左移一列",
            "\033[{n}A": "光标上移 n 行",
            "\033[{n}B": "光标下移 n 行",
            "\033[{n}C": "光标右移 n 列",
            "\033[{n}D": "光标左移 n 列",
        },
        "屏幕擦除": {
            "\033[J": "清除从光标到屏幕末尾",
            "\033[0J": "清除从光标到屏幕末尾",
            "\033[1J": "清除从屏幕开始到光标",
            "\033[2J": "清除整个屏幕",
            "\033[K": "清除从光标到行尾",
            "\033[0K": "清除从光标到行尾",
            "\033[1K": "清除从行首到光标",
            "\033[2K": "清除整行",
        },
        "文本属性": {
            "\033[0m": "重置所有属性",
            "\033[1m": "粗体/加亮",
            "\033[4m": "下划线",
            "\033[5m": "闪烁",
            "\033[7m": "反显",
            "\033[22m": "正常强度",
            "\033[24m": "非下划线",
            "\033[25m": "非闪烁",
            "\033[27m": "非反显",
        },
        "颜色控制": {
            "\033[30m": "黑色前景",
            "\033[31m": "红色前景",
            "\033[32m": "绿色前景",
            "\033[33m": "黄色前景",
            "\033[34m": "蓝色前景",
            "\033[35m": "品红前景",
            "\033[36m": "青色前景",
            "\033[37m": "白色前景",
            "\033[40m": "黑色背景",
            "\033[41m": "红色背景",
            "\033[42m": "绿色背景",
            "\033[43m": "黄色背景",
            "\033[44m": "蓝色背景",
            "\033[45m": "品红背景",
            "\033[46m": "青色背景",
            "\033[47m": "白色背景",
        },
        "设备查询": {
            "\033[c": "查询设备属性 (DA1)",
            "\033[>c": "查询次设备属性 (DA2)",
            "\033[6n": "查询光标位置 (CPR)",
            "\033[5n": "查询设备状态",
        },
        "模式设置": {
            "\033[?1h": "设置应用光标键模式",
            "\033[?1l": "重置光标键模式",
            "\033[?3h": "设置 132 列模式",
            "\033[?3l": "设置 80 列模式",
            "\033[?5h": "设置反显模式",
            "\033[?5l": "重置反显模式",
            "\033[?6h": "设置原点模式",
            "\033[?6l": "重置原点模式",
            "\033[?7h": "设置自动换行",
            "\033[?7l": "重置自动换行",
            "\033[?25h": "显示光标",
            "\033[?25l": "隐藏光标",
        },
    }

    # VT220 技术规格
    SPECIFICATIONS = {
        "发布年份": "1983",
        "制造商": "Digital Equipment Corporation (DEC)",
        "显示": {
            "标准模式": "80 列 × 24 行",
            "宽屏模式": "132 列 × 24 行",
            "字符集": "ASCII + 国家字符集",
            "属性": "正常、粗体、下划线、闪烁、反显",
        },
        "键盘": {
            "类型": "LK201 键盘",
            "功能键": "F1-F20",
            "编辑键": "Insert, Delete, Home, End, Page Up, Page Down",
            "数字键盘": "独立数字键盘",
        },
        "通信": {
            "接口": "RS-232C",
            "波特率": "50-19200 bps",
            "数据位": "7 或 8 位",
            "停止位": "1 或 2 位",
            "校验": "无、奇、偶",
        },
        "兼容性": {
            "向后兼容": "VT100, VT52",
            "字符集": "ASCII, DEC 多国字符集, DEC 技术字符集",
        },
    }


class VT220Emulator:
    """VT220 终端模拟器"""

    def __init__(self):
        self.cursor_x = 0
        self.cursor_y = 0
        self.screen_width = 80
        self.screen_height = 24
        self.attributes = {
            "bold": False,
            "underline": False,
            "blink": False,
            "reverse": False,
        }

    def demonstrate_features(self):
        """演示 VT220 功能"""

        print("\n" + "=" * 70)
        print("VT220 终端功能演示")
        print("=" * 70)

        # 1. 颜色演示
        print("\n1. 颜色支持:")
        print("-" * 70)
        colors = [
            (30, "黑色"),
            (31, "红色"),
            (32, "绿色"),
            (33, "黄色"),
            (34, "蓝色"),
            (35, "品红"),
            (36, "青色"),
            (37, "白色"),
        ]
        for code, name in colors:
            print(f"\033[{code}m■\033[0m {name}", end="  ")
        print("\n")

        # 2. 文本属性演示
        print("2. 文本属性:")
        print("-" * 70)
        print(f"\033[1m粗体文本\033[0m")
        print(f"\033[4m下划线文本\033[0m")
        print(f"\033[7m反显文本\033[0m")
        print(f"\033[1m\033[4m粗体+下划线\033[0m")
        print()

        # 3. 光标控制演示
        print("3. 光标控制:")
        print("-" * 70)
        print("保存光标位置: \\033[s")
        print("恢复光标位置: \\033[u")
        print("移动到 (10,5): \\033[10;5H")
        print()

        # 4. 屏幕控制
        print("4. 屏幕控制:")
        print("-" * 70)
        print("清屏: \\033[2J")
        print("清除到行尾: \\033[K")
        print("清除整行: \\033[2K")
        print()


def parse_vt220_response(response: str) -> Dict:
    """解析 VT220 设备属性响应"""

    # 移除 ESC 和 CSI 前缀
    content = response
    if content.startswith("\033[") or content.startswith("\x1b["):
        content = content[2:]

    # 检查私有标记
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

    # 检查是否为 VT220
    is_vt220 = 62 in params or 61 in params

    # 解析属性
    attributes = []
    for param in params:
        attr_info = VT220Terminal.VT220_ATTRIBUTES.get(
            param,
            {
                "name": f"未知属性 ({param})",
                "description": "未记录的属性",
                "category": "其他",
            },
        )
        attributes.append({"code": param, **attr_info})

    # 按类别分组
    by_category = {}
    for attr in attributes:
        category = attr.get("category", "其他")
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(attr)

    return {
        "raw_response": response,
        "is_vt220": is_vt220,
        "terminal_level": (
            "VT220" if 62 in params else ("VT100" if 61 in params else "未知")
        ),
        "parameters": params,
        "attributes": attributes,
        "by_category": by_category,
    }


def display_vt220_info(parsed_data: Dict):
    """显示 VT220 详细信息"""

    print("\n" + "=" * 70)
    print("VT220 终端属性详细报告")
    print("=" * 70)

    print(f"\n原始响应: {repr(parsed_data['raw_response'])}")
    print(f"终端级别: {parsed_data['terminal_level']}")
    print(f"是否为 VT220: {'是' if parsed_data['is_vt220'] else '否'}")
    print(f"参数列表: {parsed_data['parameters']}")

    print("\n按类别分组的功能:")
    print("=" * 70)

    for category, attrs in parsed_data["by_category"].items():
        print(f"\n【{category}】")
        print("-" * 70)
        for attr in attrs:
            print(f"  [{attr['code']:3d}] {attr['name']}")
            print(f"        {attr['description']}")

    print("\n" + "=" * 70)


def display_vt220_specs():
    """显示 VT220 技术规格"""

    print("\n" + "=" * 70)
    print("VT220 技术规格")
    print("=" * 70)

    specs = VT220Terminal.SPECIFICATIONS

    print(f"\n发布年份: {specs['发布年份']}")
    print(f"制造商: {specs['制造商']}")

    print("\n显示特性:")
    print("-" * 70)
    for key, value in specs["显示"].items():
        print(f"  {key}: {value}")

    print("\n键盘特性:")
    print("-" * 70)
    for key, value in specs["键盘"].items():
        print(f"  {key}: {value}")

    print("\n通信特性:")
    print("-" * 70)
    for key, value in specs["通信"].items():
        print(f"  {key}: {value}")

    print("\n兼容性:")
    print("-" * 70)
    for key, value in specs["兼容性"].items():
        print(f"  {key}: {value}")


def display_control_sequences():
    """显示 VT220 控制序列"""

    print("\n" + "=" * 70)
    print("VT220 控制序列参考")
    print("=" * 70)

    for category, sequences in VT220Terminal.CONTROL_SEQUENCES.items():
        print(f"\n【{category}】")
        print("-" * 70)
        for seq, desc in sequences.items():
            # 转义显示
            display_seq = (
                seq.replace("\033", "\\033").replace("{", "{").replace("}", "}")
            )
            print(f"  {display_seq:25s} - {desc}")


def test_vt220_compatibility():
    """测试当前终端的 VT220 兼容性"""

    print("\n" + "=" * 70)
    print("VT220 兼容性测试")
    print("=" * 70)

    tests = [
        ("颜色支持", "\033[31m红色\033[0m", "显示红色文本"),
        ("粗体", "\033[1m粗体\033[0m", "显示粗体文本"),
        ("下划线", "\033[4m下划线\033[0m", "显示下划线文本"),
        ("反显", "\033[7m反显\033[0m", "显示反显文本"),
        ("光标隐藏/显示", "\033[?25l隐藏\033[?25h", "光标应该短暂隐藏"),
    ]

    print("\n正在执行兼容性测试...\n")

    for i, (name, sequence, expected) in enumerate(tests, 1):
        print(f"{i}. {name}:")
        print(f"   输出: {sequence}")
        print(f"   预期: {expected}")
        print()


def main():
    """主函数"""

    print("=" * 70)
    print("VT220 终端完整解析工具")
    print("=" * 70)

    # 显示菜单
    print("\n请选择功能:")
    print("1. 显示 VT220 技术规格")
    print("2. 显示 VT220 控制序列")
    print("3. 演示 VT220 功能")
    print("4. 测试 VT220 兼容性")
    print("5. 解析示例响应")
    print("6. 显示全部信息")

    choice = input("\n请输入选项 (1-6): ").strip()

    if choice == "1":
        display_vt220_specs()

    elif choice == "2":
        display_control_sequences()

    elif choice == "3":
        emulator = VT220Emulator()
        emulator.demonstrate_features()

    elif choice == "4":
        test_vt220_compatibility()

    elif choice == "5":
        # 使用示例响应
        example_response = "\033[?62;1;2;6;7;8;9c"
        print(f"\n使用示例响应: {repr(example_response)}")
        parsed = parse_vt220_response(example_response)
        display_vt220_info(parsed)

    elif choice == "6":
        display_vt220_specs()
        display_control_sequences()
        emulator = VT220Emulator()
        emulator.demonstrate_features()
        test_vt220_compatibility()

        example_response = "\033[?62;1;2;6;7;8;9c"
        parsed = parse_vt220_response(example_response)
        display_vt220_info(parsed)

    else:
        print("无效选项")

    print("\n" + "=" * 70)


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
