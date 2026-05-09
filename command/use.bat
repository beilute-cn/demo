@echo off

:: 不是直接添加，应该是没有才添加，删除也是，只有包含时才删除

set old_ARMGCC_DIR=%ARMGCC_DIR%
set old_PATH=%PATH%

set ARMGCC_DIR=C:\sys\exe\arm-gnu-toolchain
set PATH=C:\sys\exe\arm-gnu-toolchain\bin;%PATH%

arm-none-eabi-gcc.exe -v

prompt $P (arm gnu 14.3) $G