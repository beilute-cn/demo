def E(n):
    if not n:
        return -1
    e = 1
    while not (n & e):
        e <<= 1
    return e


def f(n):
    while True:
        print(f"{n}")
        e = E(n)
        if e == n:
            return
        n = 3 * n + e


for i in range(19, 29):
    n = 3 * i + E(i)
    print(f"{i}\t{n}\t{i^n}")
