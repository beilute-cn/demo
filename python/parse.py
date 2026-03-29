import re


class Parse:
    @staticmethod
    def west():
        pass

    @staticmethod
    def west_build(
        command: str = None, arguments: dict[str, str] = None
    ) -> dict[str, str] | str | None:
        if command is not None:
            r = {}
            t = re.split(r"[ =]", command)
            if t[0] == "west" and t[1] == "build":
                pass
            else:
                print("不是west build开头")
                return None
            i = 2
            while i < len(t):
                if t[i].startswith("-"):
                    if t[i] == "--sysbuild":
                        r["--sysbuild"] = None
                    elif i == (len(t) - 1):
                        print(f"这是最后一个参数，没有值")
                        return None
                    else:
                        r[t[i]] = t[i + 1]
                        # 额外移动一次
                        i += 1
                else:
                    if re.fullmatch(r"[a-zA-Z/_0-9]*", t[i]):
                        if None not in r:
                            r[None] = t[i]
                        else:
                            print(f"多个目录，无参数键")
                            return None
                    else:
                        print("不是目录")
                        return None
                i += 1
            return r
        # 项目参数
        elif arguments is not None:
            r = ["west", "build"]
            for k, v in arguments.items():
                # 项目路径
                if k is None:
                    if v is not None and re.fullmatch(r"[a-zA-Z/_0-9]*", v):
                        r.append(v)
                    else:
                        print("项目路径格式错误")
                        return None
                # 无值参数 --sysbuild
                elif v is None:
                    if k is not None and k == "--sysbuild":
                        r.append(k)
                    else:
                        print("无值参数格式（{k}）错误，非--sysbuild")
                        return None
                elif not re.fullmatch(r"-\S*", k):
                    print(f"参数键（{k}）不符合")
                    return None
                elif not re.fullmatch(r"\S*", v):
                    print(f"参数值（{v}）不符合")
                    return None
                else:
                    r.append(f"{k}={v}")
            return " ".join(r)
        else:
            print("两个参数都是None")

    @staticmethod
    def west_build2(command: str) -> dict[str, str]:
        r"""
         *west *build( +(-[^=]*)?(?:=| *)(\S+))+ *

        可能的空格 + west + 必然的空格 + build +
            多个（必然的空格 + 必然的参数键值对） +
        可能的空格

        必然的空格 + 必然的参数键值对
             +(-[^=]*)?(?:=| *)(\S+)
            键
                以-开头的，不含等号和空格的字符串字符串
                可选 -> 项目路径，没有键
            连接
                = 或者 至少一个空格
            值
                必然存在的字符串 -> 值可能为空，若值也为空，会匹配上最后的一些空格，值必不为空
        """
        # print(re.fullmatch(r" *west +build( +(-[^= ]*)?(?:=| *)(\S+))+ *", command))
        t = re.match(r" *west +build", command)

        # 删除west和build，防止被误匹配
        t = command[t.end() :]

        result = re.findall(r" +(-[^= ]*)?(?:=| *)(\S+)", t)

        # 检查，最多只有一个为空，且一定为项目路径
        cnt = sum(t[0] == "" for t in result)
        assert (
            cnt == 1
        ), f"{cnt=}，应该有且只有一个项目路径没有参数的键，只有值。{result}"

        d = dict(result)
        d = dict(sorted(d.items()))
        return d


if __name__ == "__main__":

    command = "   west build examples_int/unit_tests/flexio/flexio_basic_register -b=kw47evk -p=always -d=build/armgcc_kw47evk/flexio_basic_register --toolchain=armgcc -Dcore_id=cm33_core0 -DCONFIG_MCUX_COMPONENT_utilities.gcov=y      -abcd  1234   --xyz=test "
    print(f"测试处理west命令，获取参数\n{command}")

    d = Parse.west(command)

    key_width, value_width = (
        max(len(k) for k in d.keys()),
        max(len(v) for v in d.values()),
    )

    print("\n" * 3)

    print(f"-" * (key_width + value_width + 3))
    for k, v in d.items():
        print(f"{k:{key_width}} | {v:<{value_width}}")
    print(f"-" * (key_width + value_width + 3))
