@echo off

set ARMGCC_DIR=%old_ARMGCC_DIR%
set PATH=%old_PATH%

set old_ARMGCC_DIR=""
set old_PATH=""

arm-none-eabi-gcc.exe -v