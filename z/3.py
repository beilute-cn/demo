def E(n):
    t = 1
    while not (n & t):
        t <<= 1
    return t


n = 19
for i in range(100):
    print(f"[{i:4}]  {n:10}")
    e = E(n) - 1
    if e == n:
        break
    n = 3 * n + e
