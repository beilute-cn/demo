"""
常用微软文档快速链接
"""

QUICK_LINKS = {
    "Excel 对象模型": {
        "Application": "https://learn.microsoft.com/en-us/office/vba/api/excel.application(object)",
        "Workbook": "https://learn.microsoft.com/en-us/office/vba/api/excel.workbook",
        "Worksheet": "https://learn.microsoft.com/en-us/office/vba/api/excel.worksheet",
        "Range": "https://learn.microsoft.com/en-us/office/vba/api/excel.range(object)",
        "Cells": "https://learn.microsoft.com/en-us/office/vba/api/excel.range.cells",
        "Chart": "https://learn.microsoft.com/en-us/office/vba/api/excel.chart(object)",
    },
    
    "常用方法": {
        "SaveAs": "https://learn.microsoft.com/en-us/office/vba/api/excel.workbook.saveas",
        "Open": "https://learn.microsoft.com/en-us/office/vba/api/excel.workbooks.open",
        "Find": "https://learn.microsoft.com/en-us/office/vba/api/excel.range.find",
        "Sort": "https://learn.microsoft.com/en-us/office/vba/api/excel.range.sort",
        "AutoFilter": "https://learn.microsoft.com/en-us/office/vba/api/excel.range.autofilter",
    },
    
    "枚举常量": {
        "XlFileFormat": "https://learn.microsoft.com/en-us/office/vba/api/excel.xlfileformat",
        "XlHAlign": "https://learn.microsoft.com/en-us/office/vba/api/excel.xlhalign",
        "XlVAlign": "https://learn.microsoft.com/en-us/office/vba/api/excel.xlvalign",
        "XlBorderWeight": "https://learn.microsoft.com/en-us/office/vba/api/excel.xlborderweight",
        "XlChartType": "https://learn.microsoft.com/en-us/office/vba/api/excel.xlcharttype",
    }
}

def print_quick_links():
    print("=" * 80)
    print("微软 Excel VBA 文档快速链接")
    print("=" * 80)
    
    for category, links in QUICK_LINKS.items():
        print(f"\n{category}:")
        print("-" * 80)
        for name, url in links.items():
            print(f"  {name:20} {url}")

if __name__ == "__main__":
    print_quick_links()
