#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="test_argparse",
        description="演示 argparse 不同 nargs 参数的效果",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s file1.txt file2.txt file3.txt
  %(prog)s --single value1
  %(prog)s --optional
  %(prog)s --optional value1
  %(prog)s --multiple val1 val2 val3
  %(prog)s --at-least-one val1 val2
  %(prog)s --exactly-two val1 val2
        """,
    )

    # 1. 位置参数 - nargs='*' (0个或多个)
    parser.add_argument(
        "files", nargs="*", metavar="FILE", help="输入文件列表 (可以0个或多个)"
    )

    # 2. 位置参数 - nargs='+' (至少1个)
    parser.add_argument(
        "required_files",
        nargs="+",
        metavar="REQUIRED_FILE",
        help="必需的文件列表 (至少1个)",
    )

    # 3. 选项参数 - 默认 (单个值)
    parser.add_argument("--single", metavar="VALUE", help="单个值参数")

    # 4. 选项参数 - nargs='?' (可选值)
    parser.add_argument(
        "--optional",
        nargs="?",
        const="DEFAULT_CONST",
        default="DEFAULT_VALUE",
        metavar="OPTIONAL_VALUE",
        help="可选值参数 (不带参数时使用 const, 完全不指定时使用 default)",
    )

    # 5. 选项参数 - nargs='*' (0个或多个)
    parser.add_argument(
        "--multiple", nargs="*", metavar="VALUE", help="多个值参数 (可以0个或多个)"
    )

    # 6. 选项参数 - nargs='+' (至少1个)
    parser.add_argument(
        "--at-least-one", nargs="+", metavar="VALUE", help="至少一个值参数"
    )

    # 7. 选项参数 - nargs=2 (恰好2个)
    parser.add_argument(
        "--exactly-two", nargs=2, metavar=("FIRST", "SECOND"), help="恰好两个值参数"
    )

    # 8. 选项参数 - action='append' (可以多次指定)
    parser.add_argument(
        "--filter",
        "-f",
        action="append",
        metavar="PATTERN",
        help="过滤模式 (可以多次指定)",
    )

    # 9. 选项参数 - action='store_true' (布尔标志)
    parser.add_argument("--verbose", "-v", action="store_true", help="启用详细输出")

    # 10. 选项参数 - action='count' (计数)
    parser.add_argument(
        "--debug",
        "-d",
        action="count",
        default=0,
        help="调试级别 (可以多次指定: -d, -dd, -ddd)",
    )

    # 11. 选项参数 - choices (限定选择)
    parser.add_argument(
        "--format",
        choices=["json", "xml", "html", "text"],
        default="text",
        help="输出格式",
    )

    # 12. 选项参数 - type (类型转换)
    parser.add_argument(
        "--count", type=int, default=10, metavar="N", help="数量 (整数)"
    )

    args = parser.parse_args()

    # 打印解析结果
    print("=" * 60)
    print("解析结果:")
    print("=" * 60)
    for key, value in vars(args).items():
        print(f"{key:20s} = {value}")
    print("=" * 60)


if __name__ == "__main__":
    main()
