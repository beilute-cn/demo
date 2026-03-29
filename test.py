import sys


class a_3n1:

    def __init__(self, n: int):
        self.n = n
        self.count = -1
        self.powers = []
        self.end = -1

        def E(n: int) -> int:
            if n <= 0:
                raise ValueError("n must be a positive integer")
            t = 1
            while not (n & t):
                t <<= 1
            return t

        while True:
            e = E(n)
            if e == n:
                break
            n = 3 * n + e

    def __str__(self):
        return f"a"


t = a_3n1(10)
print(t)

sys.exit(-1)
