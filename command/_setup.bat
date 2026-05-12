@echo off

setlocal enabledelayedexpansion

chcp 65001

:: 启用 ANSI 转义序列支持
@REM reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

:: 定义颜色代码（使用 ESC 字符）
:: 创建 ESC 字符
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "RESET=%ESC%[0m"

echo %RED%red text%RESET%

:: TODO 指定命令名称，默认为T

echo cmdcmdline = %cmdcmdline%
echo comspec--  = %comspec%

:: 不区分system32的大小写
:: 对于可能包含特殊字符、空格、引号的变量，使用 !variable!
if /i "!cmdcmdline!" == "!comspec!" (
  echo 在命令行调用
  doskey T=python "%cd%"\index.py $*
  ) else (
  echo 双击脚本文件
  :: 关闭窗口后失效，不需要禁用命令
  where wt >nul 2>nul
  if !errorlevel! equ 0 (
    echo win11使用windows terminal
    wt cmd /k doskey T=python "%cd%"\index.py $*
    goto :eof
    ) else (
    echo win10没有windows terminal
    cmd /k doskey T=python "%cd%"\index.py $*
  )
)

@REM echo 取消
@REM doskey T=
pause

goto :eof
