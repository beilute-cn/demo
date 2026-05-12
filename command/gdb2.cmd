@echo off

title 45 gdb server %date% %time%
JLinkGDBServerCL -if SWD -device KW45B41Z83
