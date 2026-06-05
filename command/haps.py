import shutil
from pathlib import Path
import sys
import os
import inspect
import re


def get_line_number():
    """获取调用此函数的行号"""
    return inspect.currentframe().f_back.f_lineno


# 工程信息：编译器、目标、根目录等
project = {}
# 要复制的所有文件和文件夹
files = {}
# sdk路径
sdk = None
# 保存到目标路径，当前文件夹，添加haps前缀
dest = f"./haps_{Path.cwd().name}"

compiler = None
board = None


# 1. 从当前路径下的cmake缓存文件读取项目信息
# 设置sdk路径
def read_project_information_from_cmakecache_file():
    cache = [f for f in Path(".").glob("CMakeCache.txt")]
    n = len(cache)
    if n == 0:
        print(f"未找到CMakeCache.txt文件")
        sys.exit(-get_line_number())
    elif n > 1:
        print(f"找到 {n} 个CMakeCache.txt文件")
        sys.exit(-get_line_number())

    cache = cache[0]

    with open(cache, "r") as f:
        lines = f.readlines()
        for line in lines:
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
    global sdk
    global compiler
    global board

    compiler = project["CONFIG_TOOLCHAIN"]["value"]
    board = project["board"]["value"]

    sdk = project["SdkRootDirPath"]["value"]  # "C:/mcux/mcuxsdk/"
    # 保留CmakeCache.txt文件，从中读取项目信息
    cache_path = cache.absolute().as_posix()

    # 对于armgcc工程，不会重新编译，将所有文件复制到同级目录
    match compiler:
        case "armgcc":
            files[cache_path] = dest + "/source/" + cache.name
        case "iar":
            files[cache_path] = cache_path.replace(sdk, dest)
        case _:
            print(f"未知的编译器: {compiler}")
            sys.exit(-get_line_number())


# 2. 从当前路径下的源文件列表读取要复制的文件
def read_source_files_from_source_list_file():
    source = [f for f in Path(".").glob("*_source_list.txt") if "exclude" not in f.name]

    n = len(source)

    if n == 0:
        print(f"未找到源文件列表")
        sys.exit(-get_line_number())
    elif n > 1:
        print(f"找到 {n} 个源文件列表：")
        for index, file in enumerate(source):
            print(f"{index}. {file}")
        sys.exit(-get_line_number())

    # 有且仅有一个文件
    source = source[0]

    with open(source, "r") as f:
        # 源文件列表中的所有文件

        for file in f.read().split(";"):
            if file in files:
                print(f"文件已存在: {file}")
                continue
            # 对于armgcc工程，不会重新编译，将所有文件复制到同级目录
            match compiler:
                case "armgcc":
                    files[file] = dest + "/source/" + Path(file).name
                case "iar":
                    files[file] = file.replace(sdk, dest)
                case _:
                    print(f"未知的编译器: {compiler}")
                    sys.exit(-get_line_number())


# 3. 对特定编译器/板卡需要的额外文件
def extra():

    # 针对不同的编译器
    # 对于iar编译器，包含iar路径
    if compiler == "iar":
        iar = Path("./iar/")
        if iar.exists():
            for i in [f for f in iar.glob("*.ew*")]:
                i_path = i.absolute().as_posix()
                files[i_path] = i_path.replace(sdk, dest)
        else:
            print(f"当前编译器是iar，但是没有iar目录")

    # 对于armgcc编译器，包含elf文件
    elif compiler == "armgcc":
        elf = list(Path(".").glob("*.elf"))
        n = len(elf)
        if n == 0:
            print(f"未找到elf文件")
        elif n > 1:
            print(f"找到 {n} 个elf文件")
            for index, file in enumerate(elf):
                print(f"{index}. {file}")
        # 只有一个elf文件
        elf = elf[0]
        elf_path = elf.absolute().as_posix()
        files[elf_path] = dest + "/" + elf.name

    else:
        print(f"未知的编译器: {compiler}")
        sys.exit(-get_line_number())

    # ------------------------

    # 针对不同的板卡
    temp = []
    if board == "frdmmcxc353":
        temp = [f"{sdk}/devices_int/MCX/MCXC/MCXC353/iar/MCXC353_ram.icf"]
        for f in temp:
            match compiler:
                case "armgcc":
                    files[file] = dest + "/source/" + Path(f).name
                case "iar":
                    files[f] = f.replace(sdk, dest)
                case _:
                    print(f"未知的编译器: {compiler}")
                    sys.exit(-get_line_number())
    elif board == "mimxrt2660evk":
        temp = [f"{sdk}/devices_int/RT/RT2660/MIMXRT2662/drivers/fsl_memory.h"]
        for f in temp:
            files[f] = f.replace(sdk, dest)
            match compiler:
                case "armgcc":
                    files[f] = dest + "/source/" + Path(f).name
                case "iar":
                    files[f] = f.replace(sdk, dest)
                case _:
                    print(f"未知的编译器: {compiler}")
                    sys.exit(-get_line_number())
        # 对iar工程添加，ozone命令和jlink脚本
        files[r"C:\Users\nxg13559\OneDrive - NXP\haps_1\rt2660\debug"] = f"{dest}/" + (
            f"build/{Path.cwd().name}/iar" if compiler == "iar" else ""
        )
        # 对armgcc工程，打开并保存
        # TODO
        # 在文件复制之后，再打开
        # print(f"{compiler=}")
        # if compiler == "armgcc":
        #     print(f"hello world")
        #     os.system(f'(cd "{dest}") & (z)')

    elif board == "kw47evk":
        pass
    elif board == "frdmmcxw72":
        pass
    elif board == "frdmmcxn947":
        pass
    else:
        print(f"未知的板卡: {board}")
        sys.exit(-get_line_number())


def copy_all_files_and_folders():
    # TODO 每次清空这个目录，当前无法删除iar目录
    if False:
        temp = Path(dest)
        if temp.exists():
            print(f"{dest}已经存在，将被删除")
            shutil.rmtree(temp)

    print(f"从【{sdk}】复制所有需要的文件到【{dest}】")
    i = 1
    n = len(files)
    for s, d in files.items():
        print(f"[{i} / {n}]" + ("\n" if i == n else "\r"), end="", flush=True)
        source = Path(s)
        destination = Path(d)
        destination.parent.mkdir(parents=True, exist_ok=True)
        # print(f"{source} -> {destination}")
        if source.is_file():
            shutil.copy2(source, destination)
        elif source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            print(f"警告: 文件或目录不存在: {source}")
        i += 1


def print_all_files():
    i = 0
    for s, d in files.items():
        print(f"{i}.{s}\n" f"\t-> {d}")
        i += 1


if __name__ == "__main__":
    read_project_information_from_cmakecache_file()
    read_source_files_from_source_list_file()
    # files = {}
    extra()
    # print_all_files()
    copy_all_files_and_folders()

    # 在文件复制之后，再打开
    if compiler == "armgcc" and board == "mimxrt2660evk":
        print(f"hello world")
        os.system(f'(cd "{dest}") & (z)')
        # 保存工程
        jdebug = [f for f in Path(".").rglob("*.jdebug")]
        n = len(jdebug)
        if n == 0:
            print(f"未找到ozone工程文件")
            sys.exit(-get_line_number())
        elif n > 1:
            print(f"找到 {n} 个ozone工程文件")
            for index, file in enumerate(jdebug):
                print(f"{index}. {file}")
            sys.exit(-get_line_number())
        # 只有一个ozone工程文件
        jdebug = jdebug[0]
        with open(jdebug, "r+", encoding="utf-8") as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                if re.fullmatch(r" +File.Open.*\n", line):
                    # 采用相同的缩进
                    n = len(line) - len(line.lstrip())
                    lines.insert(index, f" " * n + f'Project.SetRootPath ("source")\n')
                    f.writelines(lines)
                    break
            else:
                print(f"没有找到合适的位置")
