'''
数据处理模块
读取标准化后的CSV文件，清洗数据并计算目标指标，生成指标字典
'''

import pandas as pd
import os
import numpy as np
import glob

from akshare import stock_a_code_to_symbol

# 所需的数值列表，类型统一为float
NUMERIC_COLUMNS = [
    'revenue',           # 营业收入
    'revenue_yoy',       # 营收同比增长率
    'net_profit',        # 净利润
    'net_profit_yoy',    # 净利润同比增长率
    'gross_margin',      # 销售毛利率
    'net_margin',        # 销售净利率
    'roe',               # 净资产收益率
    'debt_ratio',        # 资产负债率
    'bvps',              # 每股净资产
    'ocf_ps',            # 每股经营现金流
    'eps',               # 基本每股收益
]

# 数据读取
def data_load(filepath: str) -> pd.DataFrame:
    '''
    读取数据
    :param filepath: 数据存放的文件路径
    '''
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    print(f'已读取文件路径：{os.path.basename(filepath)}')
    print('文件形状为：', df.shape)
    return df

# 中文处理
def _convert_chinese_unit(value: str):
    """
        将带中文单位的字符串转为数字（单位：元）
    """
    if not isinstance(value, str):
        return value

    value = value.strip()

    if value in ('', 'nan', 'None', 'False', 'True'):
        return np.nan

    try:
        if '亿' in value:
            num = float(value.replace('亿', ''))
            return num * 1e8
        elif '万' in value:
            num = float(value.replace('万', ''))
            return num * 1e4
        else:
            return float(value)
    except:
        return np.nan

# 数据清洗
def data_clean(df: pd.DataFrame) -> pd.DataFrame:
    '''
    对数据进行清理，保留有效数据列，去除符号以及中文字符，转化数据为float并去除缺失值
    :param df:原始dataframe
    :return:清洗后的dataframe
    '''
    df_clean = df.copy()

    # 数据清理
    for col in NUMERIC_COLUMNS:
        if col in df_clean.columns:
            # 字符串转换
            df_clean[col] = df_clean[col].astype(str).str.strip()
            # 去除%和，
            df_clean[col] = df_clean[col].str.replace(',', '').str.replace('%', '')

            # 处理中文单位
            df_clean[col] = df_clean[col].apply(_convert_chinese_unit)
            # 转float
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    return df_clean

# 计算补充指标
def calculate_indicators(df_clean: pd.DataFrame) -> pd.DataFrame:
    '''
    计算缺失的衍生指标。
    如果某些指标在原始数据中不存在，可以用其他指标推算。
    :param df: 清洗好的数据dataframe
    :return: 包含指标的dataframe
    '''
    df_cal = df_clean.copy()

    # 如果没有net_margin（销售净利润），用 net_profit（净利润） / revenue（营业总收入） 计算
    if 'net_margin' in df_cal.columns and 'net_profit' in df_cal.columns and 'revenue' in df_cal.columns:
        data_miss = df_cal['net_margin'].isna()
        df_cal.loc[data_miss, 'net_margin'] = (
            df_cal.loc[data_miss, 'net_profit'] / df_cal.loc[data_miss, 'revenue'].replace(0,np.nan) * 100
        )

    #  如果revenue_yoy（营业总收入同比增长率）不存在，则可以用邻期的revenue计算（暂定）

    print('衍生指标完成')
    return df_cal

# 生成字典
def dict_crate(df_cal: pd.DataFrame) -> pd.DataFrame:
    '''
    通过对最新一期数据的提取，生成指标字典，以供LLM进行报告生成
    :param df_cal:衍生指标处理过后的dataframe
    :return:指标字典
    '''

    # 先利用report_date排序获取最新数据
    if 'report_date' in df_cal.columns and len(df_cal) > 1:
        df_sort = df_cal.sort_values(by = 'report_date', ascending=False)
        latest_data = df_sort.iloc[0]
    elif len(df_cal) >= 1:
        latest_data = df_cal.iloc[0]
    else :
        return {}

    stock_code = str(latest_data.get('stock_code', '')).strip()
    # 确保6位，不足前面补0
    if stock_code and stock_code != 'nan':
        stock_code = stock_code.zfill(6)

    result = {
        "company_name": str(latest_data.get('stock_name', '未知公司')),
        "stock_code": stock_code,   # 修改一下，确保是6位字符串
        "report_date": str(latest_data.get('report_date', ''))
    }

    # 对数值指标进行处理
    for col in NUMERIC_COLUMNS:
        value = latest_data.get(col)
        if value is not None and not pd.isna(value):
            result[col] = round(latest_data.get(col), 2)
        else:
            result[col] = None

    return result

# 单个公司数据处理
def process_single(filepath: str) -> dict:
    '''
    进行完整的流程：读取，清洗，指标补充，返回字典
    '''
    df = data_load(filepath)
    df_clean = data_clean(df)
    df_cal = calculate_indicators(df_clean)
    final_dict = dict_crate(df_cal)

    print("字典生成完成")
    for key,value in final_dict.items():
        print(f'{key}: {value}')

    return final_dict

# 批量处理
def process_all(data_dir: str) -> dict:
    '''
    批量处理 data目录下所有 CSV
    返回 {公司名: 指标字典}
    '''
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    results = {}

    for filepath in csv_files:
        company_name = os.path.basename(filepath).replace('.csv', '').replace('_financial','')
        print(f"\n{'=' * 50}")
        print(f"处理: {company_name}")
        print(f"{'=' * 50}")

        try:
            results[company_name] = process_single(filepath)
            print(f'{company_name}处理完成')
        except Exception as e:
            print(f'{company_name}处理失败')

    return results

if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, 'data')

    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    if csv_files:
        results = process_all(data_dir)
        print(f"\n最终指标字典:")
        for k, v in results.items():
            print(f"{k}: {v}")
    else:
        print("data 目录下没有 CSV 文件，请先运行 data_fetcher.py")
