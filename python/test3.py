import yaml
import os
from pathlib import Path
from typing import TextIO
import inspect
import subprocess
from enum import Enum
from parse import Parse
import sys
import json
import yaml
from typing import Any, List, Dict
from time import time
from datetime import date

from box import Box


def load_yaml(file: str) -> dict | None:
    with open(file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        print(json.dumps(data, indent=2))
    return data


# 是否能保住颜色
# NOTE 本来也没什么颜色


class Color(Enum):
    GRAY = "\033[90m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


def line() -> None:
    print(f"@[ {inspect.currentframe().f_back.f_lineno} ]")


def log(content: str) -> None:
    global log_file
    print(content)
    log_file.write(content + "\n")


root = r"C:\mcux2\mcuxsdk"

(Path(root) / "log").mkdir(parents=True, exist_ok=True)
log_file = open(root + "/log/" + str(date.today()) + ".log", "a", encoding="utf-8")


def default_command() -> dict[str, str]:
    return {
        None: "?",
        "--toolchain": "armgcc",
        "-DCONFIG_MCUX_COMPONENT_utilities.gcov": "y",
        "-b": "?",
        "-d": "?",
        "-p": "always",
    }


data = Box.from_yaml(filename=r"C:\sys\data\temp\demo\python\test.yaml")

log(json.dumps(data.to_dict(), indent=2))

for board in data.get("boards", default=[None]):
    if board is None:
        log("板卡为空")
        continue
    if "name" not in board or board.name is None:
        log("板卡名称缺失")
        continue
    for driver in data.get("drivers", [None]):
        if driver is None:
            log("驱动为空")
            continue
        if "name" not in driver or driver.name is None:
            log("驱动名称缺失")
            continue
        for test in driver.get("unit tests", [None]):
            if test is None:
                log("单元测试为空")
                continue
            if "project" not in test or test.project is None:
                log("单元测试项目缺失")
                continue
            if "path" not in test or test.path is None:
                log("单元测试路径缺失")
                continue

            command = default_command()

            command[None] = test.path
            command["-b"] = board.name
            command["-d"] = "/".join(
                [
                    "build",
                    "coverage",
                    (
                        (board.build if "build" in board else board.name)
                        + "_"
                        + (test.build if "build" in test else test.project)
                    ),
                ]
            )
            command.update(board.get("arguments", {}))
            command.update(test.get("arguments", {}))

            cmd = Parse.west_build(arguments=command)

            log(f"=" * 50)
            log(f"执行命令：{cmd}")
            assert Parse.west_build(cmd) is not None, "命令无法解析"
            log(f"=" * 50)
            continue

            start = time()
            # 在指定目录下运行命令
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=root,
                capture_output=True,
                text=True,
            )
            end = time()

            log(f"耗时{(end-start):.2f}秒")

            log(f"{"-"*20}{"标准输出流"}{"-"*20}")
            log(f"{Color.GRAY.value}{result.stdout}{Color.RESET.value}")

            line()

            path = Path(
                "/".join(
                    [
                        root,
                        command["-d"],
                        (test.elf if "elf" in test else test.project)
                        + (board.elf_suffix if "elf_suffix" in board else "")
                        + ".elf",
                    ]
                )
            )

            # 是否有elf文件
            log(f"检查文件<{path}>是否存在")
            log(f"{"-"*20}{"标准错误流"}{"-"*20}")
            if path.is_file():
                log(f"{Color.YELLOW.value}{result.stderr}{Color.RESET.value}")
            else:
                log(f"{Color.RED.value}{result.stderr}{Color.RESET.value}")

            line()

            print("\n" * 3)
            sys.exit(-1)
