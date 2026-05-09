import shutil
from pathlib import Path
import sys
import os

# 针对当前路径
cwd = os.getcwd()

source_list = [
    f for f in Path(".").glob("*_source_list.txt") if "exclude" not in f.name
]

n = len(source_list)

if n == 0:
    print(f"未找到源文件列表")
    sys.exit(-1)
elif n > 1:
    print(f"找到 {n} 个源文件列表：")
    for index, file in enumerate(source_list):
        print(f"{index}. {file}")
    sys.exit(-2)

# 有且仅有一个文件
source_list = source_list[0]


files = []
project = {}


# 针对不同的编译器
def compiler():
    if "CONFIG_TOOLCHAIN" not in project:
        print(f"未找到编译器配置（CONFIG_TOOLCHAIN）")
        sys.exit(-5)

    c = project["CONFIG_TOOLCHAIN"]["value"]

    # 对于iar编译器，包含iar路径
    if c == "iar":
        if Path("./iar/").exists():
            files.append(f"{cwd}/iar")
        else:
            print(f"当前编译器是iar，但是没有iar目录")

    # 对于armgcc编译器，包含elf文件
    elif c == "armgcc":
        t = list(Path(".").glob("*.elf"))
        n = len(t)
        if n == 0:
            print(f"未找到elf文件")
        elif n > 1:
            print(f"找到 {n} 个elf文件")
            for index, file in enumerate(t):
                print(f"{index}. {file}")
        # 只有一个elf文件
        t = t[0]
        files.append(f"{cwd}/{str(t)}")

    else:
        print(f"未知的编译器: {c}")


# 针对不同的板卡
def board():
    if "board" not in project:
        print(f"未找到板卡配置（board）")
        sys.exit(-6)

    b = project["board"]["value"]

    if b == "frdmmcxc353":
        # ram linker
        files.append(
            f"{project["SdkRootDirPath"]["value"]}/devices_int/MCX/MCXC/MCXC353/iar/MCXC353_ram.icf"
        )
        pass
    elif b == "mimxrt2660evk":
        files.append(
            f"{project["SdkRootDirPath"]["value"]}/devices_int/RT/RT2660/MIMXRT2662/drivers/fsl_memory.h"
        )
    elif b == "kw47evk":
        pass
    else:
        print(f"未知的板卡: {b}")
        sys.exit(-7)


with open(source_list, "r") as s:
    # 源文件列表中的所有文件
    files = s.read().split(";")

    cache = [f for f in Path(".").glob("CMakeCache.txt")]
    n = len(cache)
    if n == 0:
        print(f"未找到CMakeCache.txt文件")
        sys.exit(-3)
    elif n > 1:
        print(f"找到 {n} 个CMakeCache.txt文件")
        sys.exit(-4)

    cache = cache[0]

    with open(cache, "r") as f:
        for line in f:
            line = line.strip()

            # 跳过空行和注释行
            if not line or line.startswith("#") or line.startswith("//"):
                continue

            # 解析格式：KEY:TYPE=VALUE
            if "=" in line:
                key_part, value = line.split("=", 1)

                # 分离键和类型
                if ":" in key_part:
                    key, var_type = key_part.split(":", 1)
                else:
                    key = key_part
                    var_type = ""

                project[key] = {"type": var_type, "value": value}

    # 保留CmakeCache.txt文件，从中读取项目信息
    files.append(f"{cwd}/CMakeCache.txt")

    # 额外信息
    compiler()
    board()

    # 添加文件结束，去重、使用/、排序
    files = sorted(list(set([Path(f).as_posix() for f in files])))

    old = project["SdkRootDirPath"]["value"]  # "C:/mcux/mcuxsdk/"
    new = f"./haps_{Path.cwd().name}"

    print(f"Copy all need files: [{old}] -> [{new}]")
    i = 1
    n = len(files)
    for file in files:
        print(f"[{i} / {n}]" + ("\n" if i == n else "\r"), end="", flush=True)
        source = Path(file)
        destination = Path(file.replace(old, new))
        destination.parent.mkdir(parents=True, exist_ok=True)
        # print(f"{source} -> {destination}")
        if source.is_file():
            shutil.copy2(source, destination)
        elif source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            print(f"警告: 文件或目录不存在: {source}")
        i += 1
