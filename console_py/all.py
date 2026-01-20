from enum import IntFlag


class all(IntFlag):

    def all(self, en_zh=1):
        r = []
        v = self.value
        for key, value in self.name.items():
            if v & key:
                r.append(value[en_zh])
            v &= ~key
        if v:
            print(f"\033[31m还有未识别的{self._name}<{hex(v)}>\033[0m")
        return r

    def __str__(self):
        return "[" + " + ".join(self.all()) + "]"
