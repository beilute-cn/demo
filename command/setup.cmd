@echo off

call "%~dp0%config.cmd" enable

@REM doskey T=call "%~dp0%index.cmd" $*
doskey sdk=call "%~dp0%sdk.cmd"
doskey sdk2=call "%~dp0%sdk2.cmd"
doskey ze=call "%~dp0%zephyr.cmd"
doskey temp=call "%~dp0%temp.cmd"
doskey gdb0=call "%~dp0%gdb0.cmd"
doskey gdb1=call "%~dp0%gdb1.cmd"
doskey gdb2=call "%~dp0%gdb2.cmd"
doskey haps=python "%~dp0%haps.py"
doskey rdapeng=python "%~dp0%dapeng.py"
prompt [%command%] $P$G

call "%~dp0%config.cmd" disable
