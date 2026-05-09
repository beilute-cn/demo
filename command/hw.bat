
@echo off

cls

echo generate hello world project

:: west build examples\demo_apps\hello_world -p=always --toolchain=armgcc -b=kw47evk -Dcore_id=cm33_core0 -d=build/hello_armgcc
west build examples\demo_apps\hello_world -p=always --toolchain=iar -t=guiproject -b=kw47evk -Dcore_id=cm33_core0 -d=build/hello_iar

echo done






