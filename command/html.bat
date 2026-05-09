:: gcno / gcda -> json
:: %1 gcno / gcda path
:: %2 report.html path
:: %3 driver path
:: %4 json base path

:: json -> html
:: %1 json path

@echo off

:: 使用UTF - 8编码
chcp 65001

:: 无参数
if "%~1"=="" (
  echo hello from html.bat without arguments
  goto :eof
)

if "%~2"=="" (
  goto :json_to_html
)
goto :gcno_gcda_to_json

:hello
echo hell from html.bat for no choice
goto :eof

:: 从 json 路径生成 html 报告
:json_to_html
if not exist %1 (
  echo [%date% %time%] gcno，gcda文件所在路径不存在，%1
  goto :eof
)
gcovr --add-tracefile=%1\*\*.json --root=. --txt-metric=branch --json-pretty --output=%1\all.json
gcovr --add-tracefile=%1\all.json --root=. --txt-metric=branch --html --html-details -o=%1\index.html
%1\index.html
goto :eof

:: 从 gcno / gcda 文件生成 json 和 html 报告
:gcno_gcda_to_json
if not exist %1 (
  echo [%date% %time%] gcno，gcda文件所在路径不存在，%1
  goto :eof
)
:: 目录已经存在，删除旧文件
if exist %2 (
  rd /s /q %2
)
if exist %2 (
  echo [%date% %time%] 删除已存在文件夹失败，%2
  echo rd /s /q %2
  goto :eof
)
:: 创建文件夹
mkdir %2
:: 复制所有数据到指定路径
:: TODO 这里文件可能被其他进程占用，可能复制不成功
:: 检查文件数量，确保复制成功
for /r %1 %%j in (*.gc*) do copy %%j %2 /Y
:: 生成json
gcovr --gcov-executable=arm-none-eabi-gcov.exe --object-directory=%2 --root=%3 --txt-metric=branch --json-pretty --json-base=%4 --output=%2\coverage.json --gcov-ignore-parse-errors=negative_hits.warn
@REM --verbose
:: 生成html
gcovr --gcov-executable=arm-none-eabi-gcov.exe --object-directory=%2 --root=%3 --txt-metric=branch --html --html-details -o=%2\index.html --gcov-ignore-parse-errors=negative_hits.warn
@REM --verbose
%2\index.html

goto :eof
