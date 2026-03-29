import subprocess
import sys

jlink_exe = "JLink.exe"
jlink_args = [
    "-device",
    "kw47b42zb7_m33_0",
    "-if",
    "SWD",
    "-speed",
    "4000",
    "-autoconnect",
    "1",
    "-SelectEmuBySN",
    "1064283484",
]

process = subprocess.Popen(
    [jlink_exe] + jlink_args,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

# 发送命令
commands = [
    "erase",
    "loadfile C:\\mcux\\mcuxsdk\\build\\kw47evk\\iar\\hello_world_cm33_core0.out",
    "r",
    "g",
    "exit",
]

i = 0
for cmd in commands:
    process.stdin.write(cmd + "\n")
    process.stdin.flush()
    print(f"\033[35m{cmd}\033[0m")
    i += 1
    if i == 5:
        break

# 实时读取输出
for line in process.stdout:
    print(line, end="")

process.wait()
print(f"\n进程退出码: {process.returncode}")
