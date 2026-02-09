# 1. Microsoft Office VBA 参考文档（最常用）
"""
微软官方文档资源汇总
"""

# ===== Office VBA API 参考 =====
OFFICE_VBA_DOCS = {
    "Excel VBA 参考": "https://docs.microsoft.com/en-us/office/vba/api/overview/excel",
    "Word VBA 参考": "https://docs.microsoft.com/en-us/office/vba/api/overview/word",
    "PowerPoint VBA 参考": "https://docs.microsoft.com/en-us/office/vba/api/overview/powerpoint",
    "Outlook VBA 参考": "https://docs.microsoft.com/en-us/office/vba/api/overview/outlook",
    "Access VBA 参考": "https://docs.microsoft.com/en-us/office/vba/api/overview/access",
    "Office VBA 总览": "https://docs.microsoft.com/en-us/office/vba/api/overview/",
}

# ===== Excel 对象模型详细文档 =====
EXCEL_OBJECT_MODEL = {
    "Application 对象": "https://docs.microsoft.com/en-us/office/vba/api/excel.application(object)",
    "Workbook 对象": "https://docs.microsoft.com/en-us/office/vba/api/excel.workbook",
    "Worksheet 对象": "https://docs.microsoft.com/en-us/office/vba/api/excel.worksheet",
    "Range 对象": "https://docs.microsoft.com/en-us/office/vba/api/excel.range(object)",
    "Cells 属性": "https://docs.microsoft.com/en-us/office/vba/api/excel.range.cells",
    "Chart 对象": "https://docs.microsoft.com/en-us/office/vba/api/excel.chart(object)",
}

# ===== Windows COM/OLE 文档 =====
WINDOWS_COM_DOCS = {
    "COM 基础": "https://docs.microsoft.com/en-us/windows/win32/com/component-object-model--com--portal",
    "COM 技术参考": "https://docs.microsoft.com/en-us/windows/win32/api/_com/",
    "OLE 自动化": "https://docs.microsoft.com/en-us/windows/win32/com/ole-automation",
    "IDispatch 接口": "https://docs.microsoft.com/en-us/windows/win32/api/oaidl/nn-oaidl-idispatch",
}

# ===== Win32 API 文档 =====
WIN32_API_DOCS = {
    "Win32 API 索引": "https://docs.microsoft.com/en-us/windows/win32/apiindex/windows-api-list",
    "Windows API 参考": "https://docs.microsoft.com/en-us/windows/win32/api/",
    "进程和线程": "https://docs.microsoft.com/en-us/windows/win32/procthread/processes-and-threads",
    "文件管理": "https://docs.microsoft.com/en-us/windows/win32/fileio/file-management",
    "注册表": "https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry",
}

# ===== Office 开发文档 =====
OFFICE_DEV_DOCS = {
    "Office 开发中心": "https://developer.microsoft.com/en-us/office",
    "Office 加载项": "https://docs.microsoft.com/en-us/office/dev/add-ins/",
    "Office Scripts": "https://docs.microsoft.com/en-us/office/dev/scripts/",
}

# 打印所有文档链接
def print_all_docs():
    print("=" * 80)
    print("微软官方文档资源汇总")
    print("=" * 80)
    
    categories = [
        ("Office VBA API 参考", OFFICE_VBA_DOCS),
        ("Excel 对象模型详细文档", EXCEL_OBJECT_MODEL),
        ("Windows COM/OLE 文档", WINDOWS_COM_DOCS),
        ("Win32 API 文档", WIN32_API_DOCS),
        ("Office 开发文档", OFFICE_DEV_DOCS),
    ]
    
    for category_name, links in categories:
        print(f"\n{category_name}")
        print("-" * 80)
        for name, url in links.items():
            print(f"  {name:30} {url}")

if __name__ == "__main__":
    print_all_docs()
