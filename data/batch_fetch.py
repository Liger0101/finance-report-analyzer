from data_fetcher import fetch_and_save

stocks = [
    ("600519", "贵州茅台"),
    ("600036", "招商银行"),
    ("600276", "恒瑞医药"),
    ("002594", "比亚迪"),
    ("000002", "万科A"),
]

for code, name in stocks:
    try:
        fetch_and_save(code, name, filename=f"{name}_financial.csv")
        print(f"{name} 获取成功\n")
    except Exception as e:
        print(f"{name} 获取失败: {e}\n")