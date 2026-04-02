@echo off

setlocal enabledelayedexpansion

chcp 65001

echo cmdcmdline = %cmdcmdline%
echo comspec = %comspec%

if "!cmdcmdline!" == "!comspec!" (
    echo 在命令行调用
    doskey T=python "%cd%"\index.py $*
) else (
    echo 双击脚本文件
    where wt >nul 2>nul
    if %errorlevel% equ 0 (
        echo win10没有windows terminal
        cmd /k doskey T=python "%cd%"\index.py $*
    ) else (
        echo win11使用windows terminal
        wt cmd /k doskey T=python "%cd%"\index.py $*
    )
)

echo 按任意键退出
doskey T=
pause

goto :eof



