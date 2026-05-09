@echo off
setlocal enabledelayedexpansion

rem 启用虚拟终端处理
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

rem 获取 ESC 字符
for /f %%A in ('echo prompt $E ^| cmd') do set "esc=%%A"

rem ========== 前景色（普通） ==========
set "black=!esc![30m"
set "red=!esc![31m"
set "green=!esc![32m"
set "yellow=!esc![33m"
set "blue=!esc![34m"
set "magenta=!esc![35m"
set "cyan=!esc![36m"
set "white=!esc![37m"

rem ========== 前景色（高亮/明亮） ==========
set "bright_black=!esc![90m"
set "bright_red=!esc![91m"
set "bright_green=!esc![92m"
set "bright_yellow=!esc![93m"
set "bright_blue=!esc![94m"
set "bright_magenta=!esc![95m"
set "bright_cyan=!esc![96m"
set "bright_white=!esc![97m"

rem ========== 背景色（普通） ==========
set "bg_black=!esc![40m"
set "bg_red=!esc![41m"
set "bg_green=!esc![42m"
set "bg_yellow=!esc![43m"
set "bg_blue=!esc![44m"
set "bg_magenta=!esc![45m"
set "bg_cyan=!esc![46m"
set "bg_white=!esc![47m"

rem ========== 背景色（高亮/明亮） ==========
set "bg_bright_black=!esc![100m"
set "bg_bright_red=!esc![101m"
set "bg_bright_green=!esc![102m"
set "bg_bright_yellow=!esc![103m"
set "bg_bright_blue=!esc![104m"
set "bg_bright_magenta=!esc![105m"
set "bg_bright_cyan=!esc![106m"
set "bg_bright_white=!esc![107m"

rem ========== 文本样式 ==========
set "reset=!esc![0m"
set "bold=!esc![1m"
set "dim=!esc![2m"
set "italic=!esc![3m"
set "underline=!esc![4m"
set "blink=!esc![5m"
set "reverse=!esc![7m"
set "hidden=!esc![8m"
set "strikethrough=!esc![9m"

rem ========== 重置样式 ==========
set "reset_bold=!esc![21m"
set "reset_dim=!esc![22m"
set "reset_italic=!esc![23m"
set "reset_underline=!esc![24m"
set "reset_blink=!esc![25m"
set "reset_reverse=!esc![27m"
set "reset_hidden=!esc![28m"

rem ========== 测试显示 ==========
echo.
echo ========== 前景色（普通） ==========
echo !black!黑色 (black)!reset!
echo !red!红色 (red)!reset!
echo !green!绿色 (green)!reset!
echo !yellow!黄色 (yellow)!reset!
echo !blue!蓝色 (blue)!reset!
echo !magenta!紫色 (magenta)!reset!
echo !cyan!青色 (cyan)!reset!
echo !white!白色 (white)!reset!

echo.
echo ========== 前景色（高亮） ==========
echo !bright_black!亮黑色 (bright_black)!reset!
echo !bright_red!亮红色 (bright_red)!reset!
echo !bright_green!亮绿色 (bright_green)!reset!
echo !bright_yellow!亮黄色 (bright_yellow)!reset!
echo !bright_blue!亮蓝色 (bright_blue)!reset!
echo !bright_magenta!亮紫色 (bright_magenta)!reset!
echo !bright_cyan!亮青色 (bright_cyan)!reset!
echo !bright_white!亮白色 (bright_white)!reset!

echo.
echo ========== 背景色（普通） ==========
echo !bg_black!!white!黑色背景 (bg_black)!reset!
echo !bg_red!!white!红色背景 (bg_red)!reset!
echo !bg_green!!white!绿色背景 (bg_green)!reset!
echo !bg_yellow!!black!黄色背景 (bg_yellow)!reset!
echo !bg_blue!!white!蓝色背景 (bg_blue)!reset!
echo !bg_magenta!!white!紫色背景 (bg_magenta)!reset!
echo !bg_cyan!!black!青色背景 (bg_cyan)!reset!
echo !bg_white!!black!白色背景 (bg_white)!reset!

echo.
echo ========== 背景色（高亮） ==========
echo !bg_bright_black!!white!亮黑色背景 (bg_bright_black)!reset!
echo !bg_bright_red!!white!亮红色背景 (bg_bright_red)!reset!
echo !bg_bright_green!!black!亮绿色背景 (bg_bright_green)!reset!
echo !bg_bright_yellow!!black!亮黄色背景 (bg_bright_yellow)!reset!
echo !bg_bright_blue!!white!亮蓝色背景 (bg_bright_blue)!reset!
echo !bg_bright_magenta!!white!亮紫色背景 (bg_bright_magenta)!reset!
echo !bg_bright_cyan!!black!亮青色背景 (bg_bright_cyan)!reset!
echo !bg_bright_white!!black!亮白色背景 (bg_bright_white)!reset!

echo.
echo ========== 文本样式 ==========
echo !bold!粗体 (bold)!reset!
echo !dim!暗淡 (dim)!reset!
echo !italic!斜体 (italic)!reset!
echo !underline!下划线 (underline)!reset!
echo !blink!闪烁 (blink)!reset!
echo !reverse!反色 (reverse)!reset!
echo !strikethrough!删除线 (strikethrough)!reset!

echo.
echo ========== 组合样式 ==========
echo !bold!!red!粗体红色!reset!
echo !underline!!green!下划线绿色!reset!
echo !bg_blue!!yellow!蓝底黄字!reset!
echo !bold!!bg_red!!white!粗体红底白字!reset!
echo !italic!!cyan!斜体青色!reset!

pause

@REM -----------------------------------------------

@echo off
setlocal enabledelayedexpansion

rem 启用虚拟终端
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

rem 获取 ESC 字符
for /f %%A in ('echo prompt $E ^| cmd') do set "esc=%%A"

rem 前景色
set "black=!esc![30m"
set "red=!esc![31m"
set "green=!esc![32m"
set "yellow=!esc![33m"
set "blue=!esc![34m"
set "magenta=!esc![35m"
set "cyan=!esc![36m"
set "white=!esc![37m"

rem 高亮前景色
set "bright_red=!esc![91m"
set "bright_green=!esc![92m"
set "bright_yellow=!esc![93m"
set "bright_blue=!esc![94m"
set "bright_magenta=!esc![95m"
set "bright_cyan=!esc![96m"

rem 背景色
set "bg_red=!esc![41m"
set "bg_green=!esc![42m"
set "bg_yellow=!esc![43m"
set "bg_blue=!esc![44m"

rem 样式
set "reset=!esc![0m"
set "bold=!esc![1m"
set "underline=!esc![4m"

rem 测试
echo !red!红色!reset!
echo !green!绿色!reset!
echo !bold!!blue!粗体蓝色!reset!
echo !bg_yellow!!black!黄底黑字!reset!

pause

@REM -------------------------------------------------
@echo off
goto :main

rem ========================================
rem 颜色库初始化函数
rem ========================================
:init_colors
setlocal enabledelayedexpansion

rem 启用虚拟终端
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

rem 获取 ESC 字符
for /f %%A in ('echo prompt $E ^| cmd') do set "esc=%%A"

rem 前景色（普通）
set "black=!esc![30m"
set "red=!esc![31m"
set "green=!esc![32m"
set "yellow=!esc![33m"
set "blue=!esc![34m"
set "magenta=!esc![35m"
set "cyan=!esc![36m"
set "white=!esc![37m"

rem 前景色（高亮）
set "bright_black=!esc![90m"
set "bright_red=!esc![91m"
set "bright_green=!esc![92m"
set "bright_yellow=!esc![93m"
set "bright_blue=!esc![94m"
set "bright_magenta=!esc![95m"
set "bright_cyan=!esc![96m"
set "bright_white=!esc![97m"

rem 背景色（普通）
set "bg_black=!esc![40m"
set "bg_red=!esc![41m"
set "bg_green=!esc![42m"
set "bg_yellow=!esc![43m"
set "bg_blue=!esc![44m"
set "bg_magenta=!esc![45m"
set "bg_cyan=!esc![46m"
set "bg_white=!esc![47m"

rem 背景色（高亮）
set "bg_bright_black=!esc![100m"
set "bg_bright_red=!esc![101m"
set "bg_bright_green=!esc![102m"
set "bg_bright_yellow=!esc![103m"
set "bg_bright_blue=!esc![104m"
set "bg_bright_magenta=!esc![105m"
set "bg_bright_cyan=!esc![106m"
set "bg_bright_white=!esc![107m"

rem 样式
set "reset=!esc![0m"
set "bold=!esc![1m"
set "dim=!esc![2m"
set "italic=!esc![3m"
set "underline=!esc![4m"
set "blink=!esc![5m"
set "reverse=!esc![7m"
set "hidden=!esc![8m"
set "strikethrough=!esc![9m"

rem 导出变量到父进程
endlocal & (
    set "esc=%esc%"
    set "black=%black%"
    set "red=%red%"
    set "green=%green%"
    set "yellow=%yellow%"
    set "blue=%blue%"
    set "magenta=%magenta%"
    set "cyan=%cyan%"
    set "white=%white%"
    set "bright_black=%bright_black%"
    set "bright_red=%bright_red%"
    set "bright_green=%bright_green%"
    set "bright_yellow=%bright_yellow%"
    set "bright_blue=%bright_blue%"
    set "bright_magenta=%bright_magenta%"
    set "bright_cyan=%bright_cyan%"
    set "bright_white=%bright_white%"
    set "bg_black=%bg_black%"
    set "bg_red=%bg_red%"
    set "bg_green=%bg_green%"
    set "bg_yellow=%bg_yellow%"
    set "bg_blue=%bg_blue%"
    set "bg_magenta=%bg_magenta%"
    set "bg_cyan=%bg_cyan%"
    set "bg_white=%bg_white%"
    set "bg_bright_black=%bg_bright_black%"
    set "bg_bright_red=%bg_bright_red%"
    set "bg_bright_green=%bg_bright_green%"
    set "bg_bright_yellow=%bg_bright_yellow%"
    set "bg_bright_blue=%bg_bright_blue%"
    set "bg_bright_magenta=%bg_bright_magenta%"
    set "bg_bright_cyan=%bg_bright_cyan%"
    set "bg_bright_white=%bg_bright_white%"
    set "reset=%reset%"
    set "bold=%bold%"
    set "dim=%dim%"
    set "italic=%italic%"
    set "underline=%underline%"
    set "blink=%blink%"
    set "reverse=%reverse%"
    set "hidden=%hidden%"
    set "strikethrough=%strikethrough%"
)
goto :eof

rem ========================================
rem 主程序
rem ========================================
:main
setlocal enabledelayedexpansion

rem 初始化颜色
call :init_colors

rem 使用示例
echo !red!这是红色文字!reset!
echo !green!这是绿色文字!reset!
echo !bold!!blue!这是粗体蓝色!reset!
echo !bg_yellow!!black!这是黄底黑字!reset!

pause
