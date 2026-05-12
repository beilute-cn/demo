@echo off

title 47 gdb server %date% %time%
JLinkGDBServerCL -if SWD -device KW47B42ZB7
