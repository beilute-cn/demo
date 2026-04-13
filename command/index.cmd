@REM @echo off

:: 也可以在T.cmd中判断，使用当前文件名，不需要config.cmd
call %~dp0%\config.cmd enable

if "%~1"=="begin" (
  doskey %command%=call "%cd%\%command%.cmd" $*
  goto :end
)
if "%~1"=="end" (
  doskey %command%=
  goto :end
)
echo call index.cmd with %*

:end
call %~dp0%\config.cmd disable
goto :eof
