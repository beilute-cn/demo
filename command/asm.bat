@echo off

:: copy
copy C:\mcux2\mcuxsdk\build\frdmmcxw23\mdk\spifi_debug\mdk\flash_component_nor_spifi.bin C:\zzz\mdk_debug.bin
copy C:\mcux2\mcuxsdk\build\frdmmcxw23\mdk\spifi_release\mdk\flash_component_nor_spifi.bin C:\zzz\mdk_release.bin



:: asm

arm-none-eabi-objdump -D -b binary -m arm C:\zzz\mdk_debug.bin > C:\zzz\mdk_debug_disassembly.txt
arm-none-eabi-objdump -D -b binary -m arm C:\zzz\mdk_release.bin > C:\zzz\mdk_release_disassembly.txt


echo done

