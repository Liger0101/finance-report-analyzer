'''
项目主程序
通过输入股票代码，自动完成：取数 → 处理 → 生成报告
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processor import process_single, process_all
from llm_reporter import generate_report, save_report

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'))

from data_fetcher import fetch_and_save

def main():
    while True:
        print("\n欢迎使用本财务分析器")
        print('1. 单个文件处理')
        print('2. 多个文件批量处理')
        print('3. 处理文件夹中已存在的文件')
        print('4. 退出')
        choice = input("请选择: ").strip()

        if choice == '1':
            process_single_by_code()
        elif choice == '2':
            process_all_by_code()
        elif choice == '3':
            process_all_csv()
        elif choice == '4':
            print("再见")
            break
        else:
            print("无效选择")

def process_single_by_code():
    stock_code = input('请输入公司代码: ').strip()
    symbol = input('请输入公司简称: ').strip()
    filename = input('请输入保存文件名: ').strip()

    if filename :
        clean_df = fetch_and_save(stock_code, symbol, filename)
    else:
        clean_df = fetch_and_save(stock_code, symbol)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, 'data')

    if filename:
        csv_path = os.path.join(data_dir, filename)
    else:
        csv_path = os.path.join(data_dir, f'{symbol or stock_code}_financial.csv')

    indicator_dict = process_single(csv_path)

    report_text = generate_report(indicator_dict)

    save_report(indicator_dict, report_text)

    print(f"{symbol or stock_code} 成功\n")

def process_all_by_code():
    print("请输入股票代码和简称，每行一个，格式：代码,简称")
    print("输入空行结束：")
    print("示例：600519,贵州茅台")

    stocks = []
    while True:
        line = input().strip()
        if not line:
            break
        parts = line.split(',')
        if len(parts) == 2:
            stocks.append((parts[0].strip(), parts[1].strip()))
        elif len(parts) == 1:
            stocks.append((parts[0].strip(),None))

    if not stocks:
        print('没有任何公司')
        return

    for stock_code, company_name in stocks:
        print("=" * 50)
        print(f"获取: {company_name or stock_code}")
        print("=" * 50)

        try:
            fetch_and_save(stock_code, company_name)

            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(project_root, 'data')
            csv_path = os.path.join(data_dir, f'{company_name or stock_code}_financial.csv')

            indicator_dict = process_single(csv_path)

            report_text = generate_report(indicator_dict)

            save_report(indicator_dict, report_text)

            print(f"{company_name or stock_code} 成功\n")


        except Exception as e:
            print(f"{company_name or stock_code} 失败: {e}\n")

def process_all_csv():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, 'data')

    results = process_all(data_dir)

    if not results:
        print('处理失败')
        return

    print("\n" + "=" * 50)
    print("开始生成报告")
    print("=" * 50)

    for company_name, indicator_dict in results.items():
        try:
            report_text = generate_report(indicator_dict)

            save_report(indicator_dict, report_text)

            print(f"{company_name} 成功\n")

        except Exception as e:
            print(f"{company_name} 失败: {e}\n")

if __name__ == '__main__':
    main()