@echo off

cls

cmake -GNinja -BC:\mcux\mcuxsdk\docs\_build C:\mcux\mcuxsdk\docs
@REM -DBOARD_TARGET=kw47evk ^
@REM -DDOCGEN_BRANCH=main ^
@REM -DDOCGEN_REV="%DATE% %TIME%"

@REM cmake --trace-expand ..

set PATH=%PATH%;C:\sys\exe\doxygen-1.14.0.windows.x64.bin

ninja -C C:\mcux\mcuxsdk\docs\_build html -v
@REM --debug=explain

@REM ninja: error: unknown debug setting 'ebug=explain'

