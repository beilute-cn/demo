import subprocess
import threading
import yaml
from pathlib import Path

import json

repo = []


def f1():
    print(f"prepare")
    repo = []
    repo.append("arch")


def undo():
    pass


print(list(Path(f"C:/build/A_47_pflash_test_all").glob("*.elf")))

# exit(0)

with (
    open("./test.yaml", "r", encoding="utf-8") as file,
    open("build.log", "w", encoding="utf-8") as log,
):

    def out(string):
        print(string)
        log.write(string)
        log.write("\n")
        log.flush()

    data = yaml.safe_load(file)
    print("=" * 50)
    print(f"{yaml.dump(data,sort_keys=False)}")
    print("=" * 50)
    # print(f"{data}")
    print("=" * 50)

    f"{data["build"]}"

    for board in data["boards"]:
        default = data["default"].get(board, {})
        if board.startswith("_"):
            continue
        for driver, tests in data["drivers"].items():
            if tests is None:
                tests = {}
            if driver.startswith("_"):
                continue
            for test, config in tests.items():
                if config is None:
                    config = {}
                if test.startswith("_"):
                    continue
                path = (
                    config["path"].format(
                        board=board,
                    )
                    if "path" in config
                    else "/".join(
                        [
                            f"{data["unit test"]}",
                            f"{driver}",
                            f"{test}",
                        ]
                    )
                )
                build = f"{data["build"]}/A_{f"{default["prefix"]}_" if "prefix" in default else ""}{test}"
                command = [
                    f"west",
                    f"build",
                    path,
                    f"-b={board}",
                    f"-p=always",
                    # f"-d=build/armgcc_kw47evk/{test}", # 和表格比较
                    f"-d={build}",  # A -> armgcc, I -> IAR, M -> mdk
                    f"--toolchain=armgcc",
                    f"{config["extra"] if "extra" in config else ""}",
                ]

                if "prepare" in config:
                    t = config["prepare"]
                    x = globals()
                    if t in x:
                        x[t]()
                    else:
                        out(f"未知函数<{t=}>")
                else:
                    pass
                if "argument" in default:
                    for arg in default["argument"]:
                        command.append(arg)
                command = [x for x in command if len(x)]

                t = " ".join(command)
                out("\n" * 3)
                out("=" * 140)
                out(t)
                out("=" * 140)
                out("\n")

                process = subprocess.Popen(
                    args=command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=f"{data["sdk"]}",
                    # bufsize=1,
                )
                if False:
                    threading.Thread(
                        target=lambda stream: [
                            print(f"{line.strip()}") for line in stream
                        ],
                        args=(process.stdout,),
                        # daemon=True,
                    ).start()
                    threading.Thread(
                        target=lambda stream: [
                            print(f"\033[90m{line.strip()}\033[0m") for line in stream
                        ],
                        args=(process.stderr,),
                        # daemon=True,
                    ).start()
                stdout, stderr = process.communicate()

                out(" ".join(["=" * 40, "标准流", "=" * 40]))
                for line in stdout.splitlines():
                    out(f"{line}")
                out("\n")

                out(" ".join(["=" * 40, "错误流", "=" * 40]))
                for line in stderr.splitlines():
                    out(f"E, {line}")
                out("\n")

                print(f"{data["_build"]}/{build.replace("/build2","")}")
                if len(
                    list(
                        Path(f"{data["_build"]}/{build.replace("/build2","")}").glob(
                            "*.elf"
                        )
                    )
                ):
                    pass
                else:
                    out(f"XYZ, {path}")

print(f"done")
