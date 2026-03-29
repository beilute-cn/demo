# ELF文件类型枚举
ET_NONE = 0  # 未知类型
ET_REL = 1  # 可重定位文件
ET_EXEC = 2  # 可执行文件
ET_DYN = 3  # 共享目标文件
ET_CORE = 4  # 核心转储文件

# ELF机器架构枚举
EM_NONE = 0  # 未指定
EM_M32 = 1  # AT&T WE 32100
EM_SPARC = 2  # SPARC
EM_386 = 3  # Intel 80386
EM_68K = 4  # Motorola 68000
EM_88K = 5  # Motorola 88000
EM_860 = 7  # Intel 80860
EM_MIPS = 8  # MIPS RS3000
EM_ARM = 40  # ARM
EM_X86_64 = 62  # AMD x86-64
EM_AARCH64 = 183  # ARM 64-bit

# ELF类别枚举
ELFCLASSNONE = 0  # 无效类别
ELFCLASS32 = 1  # 32位对象
ELFCLASS64 = 2  # 64位对象

# ELF数据编码枚举
ELFDATANONE = 0  # 无效数据编码
ELFDATA2LSB = 1  # 小端
ELFDATA2MSB = 2  # 大端

# OS/ABI标识枚举
ELFOSABI_NONE = 0  # UNIX System V ABI
ELFOSABI_LINUX = 3  # Linux
ELFOSABI_ARM = 97  # ARM
ELFOSABI_STANDALONE = 255  # 独立（嵌入式）应用

# 文件类型映射
file_type_map = {
    ET_NONE: "未知类型",
    ET_REL: "可重定位文件",
    ET_EXEC: "可执行文件",
    ET_DYN: "共享目标文件",
    ET_CORE: "核心转储文件",
}

# 机器架构映射
machine_map = {
    EM_NONE: "未指定",
    EM_M32: "AT&T WE 32100",
    EM_SPARC: "SPARC",
    EM_386: "Intel 80386",
    EM_68K: "Motorola 68000",
    EM_88K: "Motorola 88000",
    EM_860: "Intel 80860",
    EM_MIPS: "MIPS RS3000",
    EM_ARM: "ARM",
    EM_X86_64: "AMD x86-64",
    EM_AARCH64: "ARM 64-bit",
}

# OS/ABI映射
osabi_map = {
    ELFOSABI_NONE: "UNIX System V ABI",
    ELFOSABI_LINUX: "Linux",
    ELFOSABI_ARM: "ARM",
    ELFOSABI_STANDALONE: "独立（嵌入式）应用",
}

with open("hello_world_cm33_core0.elf", "rb") as f:
    data = f.read(5)
    if data[0:4] != b"\x7fELF":
        raise ValueError("Not a valid ELF file")

    print(f"魔法数和其他标识（0x7f 'e' 'l' 'f'） : {data[0:4]}")
    if data[4] == 1:
        pass
    else:
        pass
    print(f"类型 : {32 if data[4]==1 else 64}位")

    if data[4] == 1:
        # 32
        data += f.read(52 - 5)
        endianness = "小" if data[5] == 1 else "大"
        print(f"数据 : {endianness}端")
        print(f"ELF版本：{data[6]}")
        osabi_value = data[7]
        osabi_desc = osabi_map.get(osabi_value, f"未知({osabi_value})")
        print(f"OS/ABI标识 : {osabi_value} ({osabi_desc})")
        print(f"ABI版本 : {data[8]}")
        print(f"填充字节 : {data[9:16]}")

        print("\n" * 3)

        file_type = int.from_bytes(data[16:18], byteorder="little")
        file_type_desc = file_type_map.get(file_type, f"未知({file_type})")
        print(f"目标文件类型 : {file_type} ({file_type_desc})")

        machine = int.from_bytes(data[18:20], byteorder="little")
        machine_desc = machine_map.get(machine, f"未知({machine})")
        print(f"目标架构 : {machine} ({machine_desc})")

        print(f"目标文件版本 : {int.from_bytes(data[20:24], byteorder='little')}")
        print(f"程序入口点 : {hex(int.from_bytes(data[24:28], byteorder='little'))}")
        print(f"程序头表偏移 : {hex(int.from_bytes(data[28:32], byteorder='little'))}")
        print(f"节头表偏移 : {hex(int.from_bytes(data[32:36], byteorder='little'))}")
        print(
            f"处理器特定标志 : {hex(int.from_bytes(data[36:40], byteorder='little'))}"
        )
        print(f"ELF头大小 : {int.from_bytes(data[40:42], byteorder='little')} 字节")
        print(
            f"程序头条目大小 : {int.from_bytes(data[42:44], byteorder='little')} 字节"
        )
        print(f"程序头条目数 : {int.from_bytes(data[44:46], byteorder='little')}")
        print(f"节头条目大小 : {int.from_bytes(data[46:48], byteorder='little')} 字节")
        print(f"节头条目数 : {int.from_bytes(data[48:50], byteorder='little')}")
        print(f"节头字符串表索引 : {int.from_bytes(data[50:52], byteorder='little')}")

        # 解析程序头表
        phoff = int.from_bytes(data[28:32], byteorder="little")
        phentsize = int.from_bytes(data[42:44], byteorder="little")
        phnum = int.from_bytes(data[44:46], byteorder="little")

        # 程序头类型映射
        pt_type_map = {
            0: "PT_NULL (未使用)",
            1: "PT_LOAD (可加载段)",
            2: "PT_DYNAMIC (动态链接信息)",
            3: "PT_INTERP (解释器路径)",
            4: "PT_NOTE (辅助信息)",
            5: "PT_SHLIB (保留)",
            6: "PT_PHDR (程序头表)",
            7: "PT_TLS (线程本地存储)",
        }

        if phnum > 0:
            print("\n" + "=" * 50)
            print("程序头表:")
            print("=" * 50)
            f.seek(phoff)
            for i in range(phnum):
                ph_data = f.read(phentsize)
                p_type = int.from_bytes(ph_data[0:4], byteorder="little")
                p_offset = int.from_bytes(ph_data[4:8], byteorder="little")
                p_vaddr = int.from_bytes(ph_data[8:12], byteorder="little")
                p_paddr = int.from_bytes(ph_data[12:16], byteorder="little")
                p_filesz = int.from_bytes(ph_data[16:20], byteorder="little")
                p_memsz = int.from_bytes(ph_data[20:24], byteorder="little")
                p_flags = int.from_bytes(ph_data[24:28], byteorder="little")
                p_align = int.from_bytes(ph_data[28:32], byteorder="little")

                p_type_desc = pt_type_map.get(p_type, f"未知({p_type})")
                flags_desc = ""
                if p_flags & 0x1:
                    flags_desc += "X"
                if p_flags & 0x2:
                    flags_desc += "W"
                if p_flags & 0x4:
                    flags_desc += "R"

                print(f"\n程序头 {i}:")
                print(f"  类型 : {p_type} ({p_type_desc})")
                print(f"  文件偏移 : {hex(p_offset)}")
                print(f"  虚拟地址 : {hex(p_vaddr)}")
                print(f"  物理地址 : {hex(p_paddr)}")
                print(f"  文件大小 : {p_filesz} 字节")
                print(f"  内存大小 : {p_memsz} 字节")
                print(f"  标志 : {hex(p_flags)} ({flags_desc})")
                print(f"  对齐 : {hex(p_align)}")

        # 解析节头表
        shoff = int.from_bytes(data[32:36], byteorder="little")
        shentsize = int.from_bytes(data[46:48], byteorder="little")
        shnum = int.from_bytes(data[48:50], byteorder="little")
        shstrndx = int.from_bytes(data[50:52], byteorder="little")

        # 节类型映射
        sht_type_map = {
            0: "SHT_NULL (未使用)",
            1: "SHT_PROGBITS (程序数据)",
            2: "SHT_SYMTAB (符号表)",
            3: "SHT_STRTAB (字符串表)",
            4: "SHT_RELA (重定位表)",
            5: "SHT_HASH (符号哈希表)",
            6: "SHT_DYNAMIC (动态链接信息)",
            7: "SHT_NOTE (注释)",
            8: "SHT_NOBITS (不占文件空间)",
            9: "SHT_REL (重定位表)",
            10: "SHT_SHLIB (保留)",
            11: "SHT_DYNSYM (动态符号表)",
        }

        if shnum > 0:
            print("\n" + "=" * 50)
            print("节头表:")
            print("=" * 50)

            # 读取字符串表节
            f.seek(shoff + shstrndx * shentsize)
            shstr_header = f.read(shentsize)
            shstr_offset = int.from_bytes(shstr_header[16:20], byteorder="little")
            shstr_size = int.from_bytes(shstr_header[20:24], byteorder="little")
            f.seek(shstr_offset)
            shstrtab = f.read(shstr_size)

            for i in range(shnum):
                f.seek(shoff + i * shentsize)
                sh_data = f.read(shentsize)
                sh_name = int.from_bytes(sh_data[0:4], byteorder="little")
                sh_type = int.from_bytes(sh_data[4:8], byteorder="little")
                sh_flags = int.from_bytes(sh_data[8:12], byteorder="little")
                sh_addr = int.from_bytes(sh_data[12:16], byteorder="little")
                sh_offset = int.from_bytes(sh_data[16:20], byteorder="little")
                sh_size = int.from_bytes(sh_data[20:24], byteorder="little")
                sh_link = int.from_bytes(sh_data[24:28], byteorder="little")
                sh_info = int.from_bytes(sh_data[28:32], byteorder="little")
                sh_addralign = int.from_bytes(sh_data[32:36], byteorder="little")
                sh_entsize = int.from_bytes(sh_data[36:40], byteorder="little")

                # 获取节名称
                name_end = shstrtab.find(b"\x00", sh_name)
                section_name = shstrtab[sh_name:name_end].decode(
                    "utf-8", errors="ignore"
                )

                sh_type_desc = sht_type_map.get(sh_type, f"未知({sh_type})")
                flags_desc = ""
                if sh_flags & 0x1:
                    flags_desc += "W"
                if sh_flags & 0x2:
                    flags_desc += "A"
                if sh_flags & 0x4:
                    flags_desc += "X"

                print(f"\n节 {i}: {section_name}")
                print(f"  类型 : {sh_type} ({sh_type_desc})")
                print(f"  标志 : {hex(sh_flags)} ({flags_desc})")
                print(f"  地址 : {hex(sh_addr)}")
                print(f"  偏移 : {hex(sh_offset)}")
                print(f"  大小 : {sh_size} 字节")
                print(f"  链接 : {sh_link}")
                print(f"  信息 : {sh_info}")
                print(f"  对齐 : {hex(sh_addralign)}")
                print(f"  条目大小 : {sh_entsize}")

    elif data[5] == 2:
        # 64
        pass
    else:
        pass
