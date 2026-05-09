import serial

if __name__ == "__main__":
    print(f"111")

    # 打开串口
    ser = serial.Serial(
        port="COM4",  # Windows: COM3, Linux: /dev/ttyUSB0
        baudrate=115200,  # 波特率
        bytesize=8,  # 数据位
        parity="N",  # 校验位: 'N'无, 'E'偶, 'O'奇
        stopbits=1,  # 停止位
        timeout=1,  # 读超时时间(秒)
    )

    # 检查串口是否打开
    if ser.is_open:
        print(f"串口 {ser.port} 已打开")

        # 写入数据
        ser.write(b"Hello\r\n")

        # 读取数据
        data = ser.read(10)  # 读取10字节
        print(f"接收: {data}")

        # 关闭串口
        ser.close()
    print(f"222")
