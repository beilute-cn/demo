with open("arduino_portenta_h7.jpeg", "rb") as f:

    n = 2
    data = f.read(2)
    print(data)

    while True:
        data = f.read(4)
        n += 4
        print(data)

        if data[0] != 0xFF:
            break

        t = data[2] << 8 | data[3] - 2
        print(f"{t=}")
        n += t
        data = f.read(t)
        print(data)

    print(n)
