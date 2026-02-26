from winpty import PtyProcess

# 1要单独字符串，解释为两个参数
# jlink "-nogui 1"
# jlink "-nogui" "1"
command = ["jlink", "-nogui", "1"]


try:
    # , dimensions=(33, 133)
    p = PtyProcess.spawn(argv="jlink -nogui 1")

    while True:
        output = p.read()
        print(output, end="", flush=True)

except KeyboardInterrupt as e:
    print("Process interrupted by user")
finally:
    # p.close()
    print("Process terminated")
