import os
import re
import subprocess

# TODO 生成的haps项目不包含CMakeCache.txt


def find_cmake_cache():
    """查找CMakeCache.txt文件"""
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):
        cache_path = os.path.join(current_dir, "CMakeCache.txt")
        if os.path.exists(cache_path):
            return cache_path
        current_dir = os.path.dirname(current_dir)
    return None


def parse_cmake_cache(cache_path):
    """解析CMakeCache.txt文件"""
    if not cache_path:
        print("Error: CMakeCache.txt path is empty")
        return None

    if not os.path.exists(cache_path):
        print(f"Error: CMakeCache.txt not found at {cache_path}")
        return None

    cache_vars = {}
    try:
        with open(cache_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    match = re.match(r"([^:]+):([^=]+)=(.*)", line)
                    if match:
                        var_name = match.group(1)
                        var_value = match.group(3)
                        cache_vars[var_name] = var_value
    except Exception as e:
        print(f"Error: Failed to read CMakeCache.txt: {e}")
        return None

    if not cache_vars:
        print("Error: No valid variables found in CMakeCache.txt")
        return None

    return cache_vars


def find_elf_or_out_files():
    """查找当前目录及子目录中的elf或out文件"""
    elf_out_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".elf") or file.endswith(".out"):
                elf_out_files.append(os.path.join(root, file))
    return elf_out_files


def determine_compiler(cache_vars):
    """根据CMakeCache.txt判断编译器"""
    if "CONFIG_TOOLCHAIN" in cache_vars:
        return cache_vars["CONFIG_TOOLCHAIN"].lower()
    return None


def main():
    # 查找并解析CMakeCache.txt
    cache_path = find_cmake_cache()
    if not cache_path:
        print("Error: CMakeCache.txt not found")
        return

    cache_vars = parse_cmake_cache(cache_path)
    if not cache_vars:
        print("Error: Failed to parse CMakeCache.txt")
        return

    # 查找elf或out文件
    elf_files = find_elf_or_out_files()
    if not elf_files:
        print("Error: No .elf or .out files found")
        return

    # 获取参数
    file_path = elf_files[0]  # 参数1: 第一个找到的elf或out文件

    # 验证文件是否存在
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    compiler = determine_compiler(cache_vars)  # 参数2: 编译器
    if not compiler:
        print("Error: Unable to determine compiler")
        return

    target = cache_vars.get("CMAKE_BUILD_TYPE", "")  # 参数3: 构建类型
    if not target:
        print("Error: CMAKE_BUILD_TYPE not found in CMakeCache.txt")
        return

    board = cache_vars.get("CACHED_BOARD", "")  # 参数4: 板子
    if not board:
        print("Error: CACHED_BOARD not found in CMakeCache.txt")
        return

    appname = cache_vars.get("CMAKE_PROJECT_NAME", "")  # 参数5: 项目名称
    if not appname:
        print("Error: CMAKE_PROJECT_NAME not found in CMakeCache.txt")
        return

    job_name = "/".join(["nxg13559", appname])  # 参数6: job名称

    # 生成命令
    cmd = f'dapeng test --file={file_path} --compiler={compiler} --target={target} --board={board} --appname={appname} --job-name="{job_name}" -T HAPS_SZ'
    print(cmd)


if __name__ == "__main__":
    main()
