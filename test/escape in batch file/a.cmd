python a.py
python a.py 123
python a.py "test" --a="b"
@REM 第一个^将第一个"转义
@REM 第二个"为字符串的开始，第二个^为字符串内容，不是续行符号
python a.py ^
"test" ^
--a="b"

@REM 双引号可以不是成对出现的
echo a " b

@REM 当^出现在字符串中时，不作为续行符
echo a " b^
x


@REM 使用小括号包括，禁用格式化，使下一行开头有空格，不转义双引号
(
python a.py ^
    "test" ^
    --a="b"
)