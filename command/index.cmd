@REM 统一在入口关闭回显，修改时打开
@REM @echo on

:: 也可以在T.cmd中判断，使用当前文件名，不需要config.cmd
call %~dp0%config.cmd enable

@REM 无子命令，显示帮助信息
if "%~1"=="" (
  echo "无参数，帮助"
  goto :end
)

@REM 跳转到子命令
@REM echo label_%~1%
@REM echo %*
@REM XXX 为什么这里需要%作为空格，传递全部参数，需要两个%
@REM 错误流输出到nul，所以不显示错误信息
@REM call :label_%~1% % %%* 2>nul
@REM 保留错误信息
call :label_%~1% % %%*
if errorlevel 1 (
  echo errorlevel = %errorlevel%
  @REM 错误状态码不为0，也可能文件不存在
  echo 标签^<label_%~1%^>不存在
  ) else (
  @REM echo "标签存在"
)
goto :end

:label_begin
doskey %command%=call "%~dp0%\index.cmd" $*
prompt [Y] $P$G
goto :eof

:label_end
doskey %command%=
prompt [ ] $P$G
goto :eof

:label_dapeng
python %~dp0%dapeng.py
goto :eof

:label_haps
@REM 双引号要包裹整个路径
python "%~dp0%haps.py"
goto :eof

:label_gdb

title gdb server

if "%~2"=="" (
  echo "未指定板卡"
  goto :eof
)

if "%~2"=="47" (
  JLinkGDBServerCL -if SWD -device KW47B42ZB7
  goto :eof
)

if "%~2"=="45" (
  JLinkGDBServerCL -if SWD -device KW45B41Z83
  goto :eof
)

echo 未知板卡：%~2%

goto :eof

::JLinkGDBServerCL -if SWD -device KW47B42ZB7 -port 2500 -USB 1069278206
@REM JLinkGDBServerCL -if SWD -device MCXW236

goto :eof

:label_sdk
title sdk %date% %time%
cd /d C:\mcux\mcuxsdk
goto :eof

:label_sdk2
title sdk2 %date% %time%
cd /d C:\mcux2\mcuxsdk
goto :eof

:label_ze
title zephyr %date% %time%
cd /d C:\zephyr\zephyr
goto :eof

:label_temp
title temp %date% %time%
cd /d C:\sys\data\temp
goto :eof

:label_command
title command %date% %time%
cd /d %~dp0%
goto :eof

:end
call %~dp0%config.cmd disable
goto :eof
