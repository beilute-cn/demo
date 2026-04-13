@echo off

:: 使用utf-8，用于中文
chcp 65001 >nul

set "command=T"
if not "%~1"=="" (
  set "command=%~1"
)

:: 输出配置信息
(
echo @echo off
echo.
echo chcp 65001 ^>nul
echo.
echo if "%%~1"=="enable" ^(
echo  set "command=%command%"
echo  goto :end
echo ^)
echo.
echo if "%%~1"=="disable" ^(
echo  set "command="
echo  goto :end
echo ^)
echo.
echo echo 无效配置
) > config.cmd

:: XXX 使用多个echo覆盖写，不需要先删除
:: 文件名可能包含空格
:: 在文件相关操作，使用双引号，使之为一个完整参数
:: 判断存在/删除/输出重定向
set "file=%command%.cmd"

:: 清除文件，重定向输出全部为追加
:: 否则，需要第一个输出为覆盖
@REM if exist "%file%" (
@REM del "%file%"
@REM  echo 删除文件后的，错误码：%errorlevel%
:: TODO 删除失败处理1
@REM if %errorlevel% neq 0 (
@REM echo 删除文件失败1：%file%
@REM )
@REM )
:: TODO 删除失败处理2
@REM if exist "%file%" (
@REM echo 删除失败2，%file%
@REM )

::  文件内容
(
echo :: [%date% %time%]
echo :: generate command file^(%file%^)
echo.
echo @echo off
echo.
echo chcp 65001 ^>nul
echo.
echo call "%cd%\index.cmd" %%*
) > "%file%"

::
echo 复制文件（%file%）到命令行包含路径
echo 调用：`call %command% ...`

pause
