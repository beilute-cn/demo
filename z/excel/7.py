import win32com.client
import time
import threading

def auto_refresh_excel(file_path, update_func, interval=5):
    """
    方法4: 自动刷新Excel - 后台线程持续更新
    
    :param file_path: Excel文件路径
    :param update_func: 更新函数，接收worksheet作为参数
    :param interval: 更新间隔（秒）
    """
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True
    
    # 打开工作簿
    abs_path = os.path.abspath(file_path)
    if os.path.exists(abs_path):
        workbook = excel.Workbooks.Open(abs_path)
    else:
        workbook = excel.Workbooks.Add()
        workbook.SaveAs(abs_path)
    
    worksheet = workbook.Worksheets(1)
    
    # 停止标志
    stop_flag = threading.Event()
    
    def update_loop():
        """更新循环"""
        counter = 0
        while not stop_flag.is_set():
            try:
                update_func(worksheet, counter)
                counter += 1
                time.sleep(interval)
            except Exception as e:
                print(f"更新错误: {e}")
                break
    
    # 启动更新线程
    update_thread = threading.Thread(target=update_loop, daemon=True)
    update_thread.start()
    
    print(f"自动更新已启动，每 {interval} 秒更新一次")
    print("按 Ctrl+C 停止更新")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止...")
        stop_flag.set()
        update_thread.join()
        workbook.Save()
        print("已保存并停止")

# 定义更新函数
def my_update_function(worksheet, counter):
    """自定义的更新逻辑"""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 更新标题
    worksheet.Cells(1, 1).Value = f"实时数据 (更新次数: {counter})"
    
    # 更新时间
    worksheet.Cells(2, 1).Value = "当前时间:"
    worksheet.Cells(2, 2).Value = current_time
    
    # 更新随机数据
    worksheet.Cells(3, 1).Value = "随机值:"
    worksheet.Cells(3, 2).Value = random.randint(1, 1000)
    
    print(f"[{current_time}] 已更新 (第 {counter} 次)")

# 使用示例
# auto_refresh_excel("auto_update.xlsx", my_update_function, interval=3)
