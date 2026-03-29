#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import subprocess
import time
import sys
import os
import signal
import logging
from datetime import datetime
import atexit

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("jlink_daemon.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


class JLinkDaemon:
    """JLink GDB Server 守护进程 (Windows)"""

    def __init__(self, check_interval=5):
        self.process_name = "JLinkGDBServerCL.exe"
        self.command = ["JLinkGDBServerCL.exe", "-if", "SWD", "-device", "KW47B42ZB7"]
        self.check_interval = check_interval  # 检查间隔（秒）
        self.process = None
        self.running = True
        self.lockfile = os.path.join(os.getenv("TEMP"), "jlink_daemon.lock")

    def is_jlink_running(self):
        """检查 JLinkGDBServerCL 是否正在运行"""
        for proc in psutil.process_iter(["name", "cmdline"]):
            try:
                # 检查进程名
                if (
                    proc.info["name"]
                    and self.process_name.lower() in proc.info["name"].lower()
                ):
                    # 进一步检查命令行参数
                    if proc.info["cmdline"]:
                        cmdline_str = " ".join(proc.info["cmdline"])
                        if "-if" in cmdline_str and "SWD" in cmdline_str:
                            logging.info(f"发现运行中的进程: PID={proc.pid}")
                            return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def start_jlink(self):
        """启动 JLinkGDBServerCL"""
        try:
            logging.info(f"启动 JLink GDB Server: {' '.join(self.command)}")

            # 在 Windows 上使用 CREATE_NEW_CONSOLE 或 CREATE_NO_WINDOW
            self.process = subprocess.Popen(
                self.command,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                # creationflags=subprocess.CREATE_NEW_CONSOLE,  # 新控制台窗口
                # 或使用 subprocess.CREATE_NO_WINDOW  # 无窗口后台运行
            )

            logging.info(f"JLink GDB Server 已启动, PID: {self.process.pid}")

            while True:
                pass

            return True

        except FileNotFoundError:
            logging.error(f"找不到 {self.process_name}，请检查路径是否正确")
            return False
        except Exception as e:
            logging.error(f"启动失败: {e}")
            return False

    def check_daemon_running(self):
        """检查守护进程是否已经在运行"""
        if not os.path.exists(self.lockfile):
            return False

        try:
            with open(self.lockfile, "r") as f:
                pid = int(f.read().strip())

            # 检查进程是否存在
            if psutil.pid_exists(pid):
                proc = psutil.Process(pid)
                if "python" in proc.name().lower():
                    logging.warning(f"守护进程已经在运行中 (PID: {pid})")
                    return True

            # 进程不存在，删除旧的锁文件
            os.remove(self.lockfile)
            return False

        except (OSError, ValueError, psutil.NoSuchProcess):
            if os.path.exists(self.lockfile):
                os.remove(self.lockfile)
            return False

    def create_lock(self):
        """创建锁文件"""
        with open(self.lockfile, "w") as f:
            f.write(str(os.getpid()))
        atexit.register(self.cleanup)

    def cleanup(self):
        """清理锁文件"""
        if os.path.exists(self.lockfile):
            try:
                os.remove(self.lockfile)
                logging.info("清理锁文件")
            except:
                pass

    def signal_handler(self, signum, frame):
        """处理退出信号"""
        logging.info("接收到退出信号，正在停止守护进程...")
        self.running = False
        self.cleanup()
        sys.exit(0)

    def run(self):
        """运行守护进程"""
        # 检查守护进程是否已经在运行
        if self.check_daemon_running():
            logging.error("守护进程已经在运行，退出")
            sys.exit(1)

        # 创建锁文件
        self.create_lock()

        # 注册信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        logging.info("JLink GDB Server 守护进程已启动")
        logging.info(f"检查间隔: {self.check_interval} 秒")
        logging.info(f"锁文件: {self.lockfile}")

        try:
            while self.running:
                if not self.is_jlink_running():
                    logging.warning("JLink GDB Server 未运行，正在启动...")
                    self.start_jlink()
                    # 等待一小段时间让进程启动
                    time.sleep(2)
                else:
                    logging.debug("JLink GDB Server 运行正常")

                # 等待下一次检查
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logging.info("接收到 Ctrl+C，正在退出...")
        finally:
            self.cleanup()
            logging.info("守护进程已停止")


def main():
    """主函数"""
    # 创建守护进程实例，每5秒检查一次
    daemon = JLinkDaemon(check_interval=5)
    daemon.run()


if __name__ == "__main__":
    main()
