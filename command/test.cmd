@echo off

@REM ----------------------------------
@REM 使用goto，跳转到子命令
@REM 检测子命令是否存在

call :a 2>nul
if errorlevel 1 (
  echo "标签a不存在"
  ) else (
  echo "标签a存在"
)

call :d 2>nul
if errorlevel 1 (
  echo "标签d不存在"
  ) else (
  echo "标签d存在"
)

@REM 如果没有重定向，会输出错误信息
call :d 2
goto :eof

@REM goto 命令失败时不会设置 errorlevel，所以 || 操作符不会触发。必须使用 if 预先验证。
@REM goto d 2>nul || goto a

:a
echo aaaa
goto :eof

:b
echo bbbb
goto :eof

:c
echo cccc
goto :eof

@REM ----------------------------------
