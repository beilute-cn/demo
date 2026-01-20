class tab:

    def __init__(self):
        self.count = 0

    def __str__(self):
        return "\t" * self.count

    def tab(self):
        self.count += 1

    def untab(self):
        self.count -= 1


tab = tab()
