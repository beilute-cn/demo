def E(n):
    t = 1
    while not (n & t):
        t <<= 1
    return t


data = []

for i in range(50):
    n = i + 1
    count = 0
    while True:
        e = E(n)
        if e == n:
            print(f"[{i+1}], [{n >> count}, {n >> (2 * count)}]")
            break
        n = 3 * n + e
        count += 1
