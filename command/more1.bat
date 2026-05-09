@echo off

echo -----------------------------------------------------

echo + iar/ielfdumparm.exe
echo + iar/ielftool.exe
echo + iar/iarchive.exe
echo.
set PATH=%PATH%;C:\iar\ewarm-9.70.2\arm\bin

echo + arm-none-eabi-ar.exe
echo ....ar ^<- arm-none-eabi-ar
doskey ar=arm-none-eabi-ar
echo + arm-none-eabi-readelf.exe
echo ....readelf ^<- arm-none-eabi-readelf
doskey readelf=arm-none-eabi-readelf
echo + arm-none-eabi-objdump.exe
echo ....objdump ^<- arm-none-eabi-objdump
doskey objdump = arm-none-eabi-objdump
echo.

set PATH=%PATH%;C:\sys\exe\arm-gnu-toolchain\bin

@REM echo + mingw/msys
@REM set PATH=%PATH%;C:\sys\exe\mingw\bin;
@REM set PATH=%PATH%;C:\sys\exe\mingw\msys\1.0\bin

echo + msys64/mingw32-make.exe
set PATH=%PATH%;C:\sys\exe\msys64\ucrt64\bin
echo ....make ^<- mingw32-make
doskey make=mingw32-make $*
echo + msys64/file.exe
set PATH=%PATH%;C:\sys\exe\msys64\usr\bin\file.exe
echo.

echo + keil/fromelf.exe
echo.
set PATH=%PATH%;C:\Keil_v5\ARM\ARMCLANG\bin

echo -----------------------------------------------------
