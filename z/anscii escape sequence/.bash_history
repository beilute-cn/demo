python -c "import sys; sys.stdout.write('默认模式输出:\n'); [sys.stdout.write(f'Line {i}\n') for i in range(3)]; input('\n按回车切换到LNM模式...'); sys.stdout.write('\033[20hLNM模式输出:\n'); [sys.stdout.write(f'Line {i}\n') for i in range(3)]; sys.stdout.write('\033[20l')"
python -c "import sys; sys.stdout.buffer.write(b'LF:    A\nB\n'); sys.stdout.buffer.write(b'CR+LF: A\r\nB\r\n'); sys.stdout.buffer.write(b'CR:    A\rB\r\n')"
python -c "import sys; print('=== 三种换行方式 ===\n'); print('1. 仅LF:'); sys.stdout.write('A\nB\nC\n'); print('\n2. 显式CR+LF:'); sys.stdout.write('A\r\nB\r\nC\r\n'); print('\n3. LNM模式:'); sys.stdout.write('\033[20hA\nB\nC\n\033[20l'); print('\n结论: 在现代终端中效果相同')"
clear
python -c "import sys; print('=== 三种换行方式 ===\n'); print('1. 仅LF:'); sys.stdout.write('A\nB\nC\n'); print('\n2. 显式CR+LF:'); sys.stdout.write('A\r\nB\r\nC\r\n'); print('\n3. LNM模式:'); sys.stdout.write('\033[20hA\nB\nC\n\033[20l'); print('\n结论: 在现代终端中效果相同')"
exit
