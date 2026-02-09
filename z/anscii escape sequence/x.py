import sys

print("默认模式输出:")
sys.stdout.write("\033[20lA\nB\n")
data1 = b"A\nB\n"
print(f"字节: {data1.hex()} = {list(data1)}\n")
print("LNM模式输出:")
sys.stdout.write("\033[20hA\nB\n\033[20l")
print(f'理论字节:{b"A\\r\\nB\\r\\n".hex()} = {list(b"A\\r\\nB\\r\\n")}')
