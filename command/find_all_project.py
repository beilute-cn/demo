import sys
from pathlib import Path

projects = """
hello_world
led_blinky_peripheral
crc
ctimer_capture
ctimer_dma_trigger
ctimer_match_example
ctimer_match_interrupt_example
ctimer_pwm_example
ctimer_pwm_interrupt_example
edma3_channel_link
edma3_interleave_transfer
edma3_memory_to_memory
edma3_memory_to_memory_transfer
edma3_memset
edma3_ping_pong_transfer
edma3_scatter_gather
edma3_wrap_transfer
error_recording
freqme_interrupt
gpio_input_interrupt
gpio_led_output
lpcmp_interrupt
lpcmp_polling
lpcmp_round_robin
lpi2c_edma_b2b_transfer_master
lpi2c_edma_b2b_transfer_slave
lpi2c_interrupt_b2b_transfer_master
lpi2c_interrupt_b2b_transfer_slave
lpi2c_polling_b2b_master
lpi2c_polling_b2b_slave
lpspi_edma_b2b_transfer_master
lpspi_edma_b2b_transfer_slave
lpspi_interrupt_b2b_master
lpspi_interrupt_b2b_slave
lpspi_loopback
lpspi_interrupt_b2b_transfer_master
lpspi_interrupt_b2b_transfer_slave
lpspi_polling_b2b_transfer_master
lpspi_polling_b2b_transfer_slave
lptmr
lpuart_edma_transfer
lpuart_interrupt
lpuart_interrupt_rb_transfer
lpuart_interrupt_transfer
lpuart_interrupt_transfer_seven_bits
lpuart_polling
lpuart_polling_seven_bits
pwm
rtc
trdc
wwdt_example
trng_random
flash_k4
""".splitlines()

# 清理空行
projects = [p.strip() for p in projects if p.strip()]

print(f"开始搜索项目...")
print(f"项目列表: {projects}")
print(f"搜索路径: C:/mcux/mcuxsdk/examples")
print("-" * 80)

r = [None] * len(projects)  # 修复: 初始化列表

cmake_files = list(Path("C:/mcux/mcuxsdk/examples").rglob("CMakeLists.txt"))
print(f"找到 {len(cmake_files)} 个 CMakeLists.txt 文件")
print("-" * 80)

scanned_count = 0

for file in cmake_files:
    scanned_count += 1
    if scanned_count % 100 == 0:
        print(f"已扫描 {scanned_count}/{len(cmake_files)} 个文件...")

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

            for i in range(len(projects)):  # 修复: range(len(projects))
                search_pattern = f"project({projects[i]} "

                if search_pattern in content:
                    r[i] = file
                    print(f"\n✓ 找到项目: {projects[i]}")
                    print(f"  文件路径: {file}")

                    # 显示匹配的行
                    for line_num, line in enumerate(content.splitlines(), start=1):
                        if search_pattern in line:
                            print(f"  [{line_num:4d}] {line.strip()}")
                    break

    except UnicodeDecodeError:
        try:
            with open(file, "r", encoding="gbk") as f:
                content = f.read()

                for i in range(len(projects)):
                    search_pattern = f"project({projects[i]} "

                    if search_pattern in content:
                        r[i] = file
                        print(f"\n✓ 找到项目: {projects[i]}")
                        print(f"  文件路径: {file}")

                        for line_num, line in enumerate(content.splitlines(), start=1):
                            if search_pattern in line:
                                print(f"  [{line_num:4d}] {line.strip()}")
                        break
        except Exception as e:
            print(f"\n✗ 读取文件失败: {file}")
            print(f"  错误: {e}")

    except Exception as e:
        print(f"\n✗ 处理文件失败: {file}")
        print(f"  错误: {e}")

print("\n" + "=" * 80)
print("搜索完成!")
print(f"总扫描文件数: {scanned_count}")
print("-" * 80)

# 输出结果汇总
print("\n结果汇总:")
for i, project in enumerate(projects):
    if r[i]:
        print(f"✓ {project:20s} -> {r[i]}")
    else:
        print(f"✗ {project:20s} -> 未找到")


print("=" * 80)

sorted_results = []
for i, project in enumerate(projects):
    sorted_results.append((project, r[i]))

sorted_results.sort(key=lambda x: x[0])


for i, project in enumerate(projects):
    print(f"{project}")


for i, project in enumerate(projects):
    print(f"{r[i]}")


print("=" * 80)
# 统计
found_count = sum(1 for x in r if x is not None)
print("\n" + "=" * 80)
print(f"找到 {found_count}/{len(projects)} 个项目")
