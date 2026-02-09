"""
Excel Application 对象参考
文档: https://docs.microsoft.com/en-us/office/vba/api/excel.application(object)
"""

import win32com.client

# Application 对象常用属性和方法
APPLICATION_REFERENCE = {
    "属性": {
        # 显示和界面
        "Visible": "Boolean - 是否显示 Excel 窗口",
        "ScreenUpdating": "Boolean - 是否更新屏幕显示",
        "DisplayAlerts": "Boolean - 是否显示警告对话框",
        "Interactive": "Boolean - 是否允许用户交互",
        "StatusBar": "String/Boolean - 状态栏文本",
        
        # 计算
        "Calculation": "XlCalculation - 计算模式 (-4105自动, -4135手动)",
        "CalculateBeforeSave": "Boolean - 保存前是否计算",
        
        # 集合
        "Workbooks": "Workbooks - 所有打开的工作簿",
        "Worksheets": "Sheets - 活动工作簿的工作表",
        "ActiveWorkbook": "Workbook - 当前活动工作簿",
        "ActiveSheet": "Worksheet - 当前活动工作表",
        "ActiveCell": "Range - 当前活动单元格",
        "Selection": "Object - 当前选择的对象",
        
        # 应用程序信息
        "Version": "String - Excel 版本号",
        "Path": "String - Excel 安装路径",
        "Name": "String - 应用程序名称",
        "Caption": "String - 窗口标题",
    },
    
    "方法": {
        # 基本操作
        "Quit()": "退出 Excel 应用程序",
        "Calculate()": "重新计算所有打开的工作簿",
        "CalculateFull()": "完全重新计算",
        
        # 文件操作
        "GetOpenFilename()": "显示打开文件对话框",
        "GetSaveAsFilename()": "显示另存为对话框",
        
        # 其他
        "Wait(Time)": "暂停执行直到指定时间",
        "OnTime(EarliestTime, Procedure)": "在指定时间运行过程",
        "InputBox(Prompt)": "显示输入框",
    }
}

# 示例代码
def demo_application():
    excel = win32com.client.Dispatch("Excel.Application")
    
    # 设置属性
    excel.Visible = True
    excel.ScreenUpdating = False
    excel.DisplayAlerts = False
    excel.Calculation = -4135  # xlCalculationManual
    
    # 获取信息
    print(f"Excel 版本: {excel.Version}")
    print(f"安装路径: {excel.Path}")
    print(f"打开的工作簿数: {excel.Workbooks.Count}")
    
    # 创建工作簿
    workbook = excel.Workbooks.Add()
    
    # 恢复设置
    excel.ScreenUpdating = True
    excel.DisplayAlerts = True
    excel.Calculation = -4105  # xlCalculationAutomatic
    
    # 清理
    workbook.Close(SaveChanges=False)
    excel.Quit()

# 打印参考
def print_reference():
    print("=" * 80)
    print("Excel Application 对象参考")
    print("文档: https://docs.microsoft.com/en-us/office/vba/api/excel.application")
    print("=" * 80)
    
    for category, items in APPLICATION_REFERENCE.items():
        print(f"\n{category}:")
        print("-" * 80)
        for name, description in items.items():
            print(f"  {name:35} {description}")

if __name__ == "__main__":
    print_reference()
