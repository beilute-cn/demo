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

@REM 双引号要包裹整个路径
@REM python "%~dp0%haps.py"

:label_command
title command %date% %time%
cd /d %~dp0%
goto :eof

:end
call %~dp0%config.cmd disable
goto :eof
