import time
import win32com.client
import os
import random
import traceback

abs_path = os.path.abspath("example.xlsx")

try:
    print("步骤1: 连接到已打开的Excel应用...")
    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
        print("  - 成功连接到已打开的Excel")
    except:
        print("  - 未找到已打开的Excel，创建新实例...")
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True
        print("  - Excel应用创建成功")

    print(f"步骤2: 查找工作簿 {abs_path}...")
    workbook = None
    print(f"  - 当前打开的工作簿数量: {excel.Workbooks.Count}")
    
    for i in range(1, excel.Workbooks.Count + 1):
        try:
            wb = excel.Workbooks(i)
            print(f"  - 检查工作簿 {i}: {wb.FullName}")
            if wb.FullName.lower() == abs_path.lower():
                workbook = wb
                print(f"  - 找到匹配的工作簿")
                break
        except Exception as e:
            print(f"  - 检查工作簿 {i} 时出错: {e}")
            continue

    if workbook is None:
        print("  - 未找到已打开的工作簿")
        if os.path.exists(abs_path):
            print(f"  - 打开现有文件: {abs_path}")
            workbook = excel.Workbooks.Open(abs_path)
            print("  - 文件打开成功")
        else:
            print(f"  - 创建新工作簿...")
            workbook = excel.Workbooks.Add()
            workbook.SaveAs(abs_path)
            print("  - 新工作簿创建并保存成功")

    print("步骤3: 获取工作表...")
    worksheet = workbook.Worksheets(1)
    print(f"  - 工作表名称: {worksheet.Name}")
    
    print("步骤4: 清除所有格式和内容...")
    worksheet.Cells.Clear()
    print("  - 清除完成")
    
    print("步骤5: 设置范围A1:Z26...")
    range_area = worksheet.Range("A1:Z26")
    print("  - 范围对象创建成功")
    
    print("步骤6: 设置背景色为白色...")
    range_area.Interior.Color = 0xFFFFFF
    print("  - 背景色设置成功")

    print("\n开始动态更新（优化版）...\n")

    # 缓存有颜色的单元格（关键优化！）
    colored_cells = set()  # 存储有颜色的单元格地址
    iteration = 0

    while True:
        iteration += 1
        start_time = time.time()
        print(f"\n--- 迭代 {iteration} ---")

        try:
            print("  关闭屏幕更新...")
            excel.ScreenUpdating = False
        except Exception as e:
            print(f"  关闭屏幕更新失败: {e}")

        try:
            # 只遍历有颜色的单元格（大幅减少遍历次数）
            cells_to_remove = set()
            print(f"  处理 {len(colored_cells)} 个有色单元格...")

            for idx, addr in enumerate(list(colored_cells)):
                try:
                    cell = worksheet.Range(addr)
                    original = int(cell.Interior.Color)
                    
                    # 将BGR转换为RGB分量
                    b = (original >> 16) & 0xFF
                    g = (original >> 8) & 0xFF
                    r = original & 0xFF

                    # 每个分量乘以2，大于等于0xff时保持为0xff
                    new_r = min(r * 2, 0xFF)
                    new_g = min(g * 2, 0xFF)
                    new_b = min(b * 2, 0xFF)

                    # 如果颜色为白色(0xFFFFFF)，移除跟踪
                    if new_r == 0xFF and new_g == 0xFF and new_b == 0xFF:
                        print(f"    单元格 {addr} 变为白色，移除")
                        cell.Interior.Color = 0xFFFFFF
                        cells_to_remove.add(addr)
                    else:
                        # 将RGB转换回BGR格式
                        new_color = (new_b << 16) | (new_g << 8) | new_r
                        cell.Interior.Color = new_color
                        if idx < 3:  # 只打印前3个
                            print(f"    单元格 {addr}: RGB({r},{g},{b}) -> RGB({new_r},{new_g},{new_b})")
                
                except Exception as e:
                    print(f"    处理单元格 {addr} 时出错: {e}")
                    traceback.print_exc()
                    cells_to_remove.add(addr)

            # 移除已变白的单元格
            colored_cells -= cells_to_remove
            print(f"  移除了 {len(cells_to_remove)} 个单元格")

            # 添加新的随机颜色单元格
            row = random.randint(1, 26)
            col = random.randint(1, 26)
            random_color = random.randint(0, 0xFFFFFF)
            
            # 将整数颜色转换为RGB分量
            r = (random_color >> 16) & 0xFF
            g = (random_color >> 8) & 0xFF
            b = random_color & 0xFF
            
            # 转换为BGR格式（Excel使用BGR）
            bgr_color = (b << 16) | (g << 8) | r

            print(f"  添加新单元格: ({row},{col}) RGB颜色: ({r},{g},{b})")
            cell = worksheet.Cells(row, col)
            cell.Interior.Color = bgr_color
            cell.Value = f"({row},{col})"

            # 添加到缓存
            cell_addr = cell.Address
            colored_cells.add(cell_addr)
            print(f"  新单元格地址: {cell_addr}")

        except Exception as e:
            print(f"  主循环出错: {e}")
            traceback.print_exc()
        finally:
            try:
                print("  恢复屏幕更新...")
                excel.ScreenUpdating = True
            except Exception as e:
                print(f"  恢复屏幕更新失败: {e}")

        elapsed = time.time() - start_time
        print(
            f"耗时: {elapsed:.3f}s | 有色单元格: {len(colored_cells)} | 新增: ({row},{col})"
        )

        sleep_time = max(0, 1.0 - elapsed)
        if sleep_time > 0:
            print(f"  休眠 {sleep_time:.3f}s...")
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\n\n程序被用户中断")
except Exception as e:
    print(f"\n\n致命错误: {e}")
    traceback.print_exc()
