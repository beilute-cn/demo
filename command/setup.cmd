@echo off

call "%~dp0%config.cmd" enable

@REM doskey T=call "%~dp0%index.cmd" $*
doskey sdk=call "%~dp0%sdk.cmd"
@REM doskey sdk2=call "%~dp0%sdk2.cmd"
@REM doskey ze=call "%~dp0%zephyr.cmd"
doskey temp=call "%~dp0%temp.cmd"
doskey gdb0=call "%~dp0%gdb0.cmd"
doskey gdb1=call "%~dp0%gdb1.cmd"
doskey gdb2=call "%~dp0%gdb2.cmd"
doskey haps=python "%~dp0%haps.py"
doskey rdapeng=python "%~dp0%dapeng.py"
doskey command=call "%~dp0%command.cmd"
@REM doskey gcc="C:\sys\exe\msys64\ucrt64\bin\gcc.exe" $*
@REM doskey g++="C:\sys\exe\msys64\ucrt64\bin\g++.exe" $*
@REM doskey make="C:\sys\exe\msys64\ucrt64\bin\mingw32-make.exe" $*
@REM  -help看所有参数
@REM 可以在字符串中主动添加其他内容来固定格式，比如：x-help
doskey ucrt="C:\sys\exe\msys64\msys2_shell.cmd" -ucrt64 -here
prompt [%command%] $P$G

call "%~dp0%config.cmd" disable
