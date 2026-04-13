import sys
import argparse

print(f"hello from {__file__}")

if False:
    print(f"所有命令行参数：{sys.argv}")

    print(f"命令行参数类型是：{type(sys.argv)}")

    for i in sys.argv:
        print(f"参数：{i}")

    for index, item in enumerate(sys.argv):
        print(f"第 {index} 个参数：{item}")

    for i in range(len(sys.argv)):
        print(f"索引 {i}：{sys.argv[i]}")


argparse = argparse.ArgumentParser(description="这是一个命令行参数解析器")

subs = argparse.add_subparsers(dest="subcommand", help="可用的命令", required=True)


class Command:
    def __init__(self, command:str, ):
    
test1 = subs.add_parser("test1", help="测试子命令1")
test1.add_argument("--key", help="键")

test2 = subs.add_parser("test2", help="测试子命令2")
test2.add_argument("--key", help="键")

# 要同时适合命令行
# html = subs.add_parser("html", help="生成")
# 复制：路径 + 路径
# html 文件名
# json base


# 1. west build
# 2. gdb
# 3. for copy
coverage = subs.add_parser("coverage")
subs2 = coverage.add_subparsers(dest="coverage_subcommand")
copy = subs2.add_parser("copy", help="复制gcno、gcda文件")
copy.add_argument("source", help="源路径，从……复制gcno、gcda文件")
copy.add_argument("destination", help="目标路径，复制到……")
# justification
copy = subs2.add_parser("collect", help="收集说明")
copy.add_argument("-f", "--file", nargs="+", help="文件")
# 4. gcov -> json
# 5. gcov -> html
# html -> files


args = argparse.parse_args()

print(args)

if args.command == "test1":
    print(f"执行 test1 命令")
    if args.key:
        print(f"test1 键值：{args.key}")
elif args.command == "test2":
    print(f"执行 test2 命令")
    if args.key:
        print(f"test2 键值：{args.key}")
elif args.command == "coverage":
    print(f"执行 coverage 命令")
    print(f"复制从 {args.source} 到 {args.destination}")
    print(f"for /r {args.source} %%j in (*.gcno) do copy %%j {args.destination} /Y")
    print(f"for /r {args.source} %%j in (*.gcda) do copy %%j {args.destination} /Y")
else:
    print(f"未知命令：{args.command}")
