'''
财报数据获取模块
利用akshare获取上市公司的财务模块，并标准化列标签
'''

import pandas as pd
import akshare as ak
import os

#1.定义标签列表
STANDARD_COLUMNS = {
    '股票代码': 'stock_code',
    '股票简称': 'stock_name',
    '报告期': 'report_date',
    '净利润': 'net_profit',
    '净利润同比增长率': 'net_profit_yoy',
    '营业总收入': 'revenue',
    '营业总收入同比增长率': 'revenue_yoy',
    '销售毛利率': 'gross_margin',
    '销售净利率': 'net_margin',
    '净资产收益率': 'roe',
    '资产负债率': 'debt_ratio',
    '每股净资产': 'bvps',
    '每股经营现金流': 'ocf_ps',
    '基本每股收益': 'eps',
}

def get_stock_financial_data(stock_code: str, symbol: str = None) -> pd.DataFrame:
    '''
    获取指定股票的财务数据

    :param stock_code:股票代码，例如‘0000002’
    :param symbol:股票简称，例如万科A
    '''
    df = ak.stock_financial_abstract_ths(symbol = stock_code)

    if symbol:
        df['股票简称'] = symbol

    print(f'原始数据形状：, {df.shape}')
    return df


def standardize_columns(df: pd.DataFrame, keep_only_standard: bool = True) -> pd.DataFrame:
    """
    参数:
        df: 原始 DataFrame
        keep_only_standard: 是否只保留 STANDARD_COLUMNS 中定义的列
                           True  -> 只保留标准列（默认）
                           False -> 保留原始所有列，但重命名能识别的列
    """
    # 列标签清理
    df.columns = [str(c).replace('\n', '').replace('\r', '').strip()
                  for c in df.columns]

    # 修复，避免出现存在相同名字时数据存放错误的情况，例如净利润的数据存到净利润同比增长率，先按字符串从长到短排序
    sorted_standard = sorted(
        STANDARD_COLUMNS.keys(),
        key=len,
        reverse=True
    )

    # 创立映射，将中文名按照标准进行映射
    rename_map = {}
    for standard_cn in sorted_standard:
        standard_en = STANDARD_COLUMNS[standard_cn]

        for col in df.columns:
            # 已经映射过的跳过
            if col in rename_map:
                continue

            # 完全匹配
            if col == standard_cn:
                rename_map[col] = standard_en
                break
            # 模糊匹配：原始列名包含标准名 或 标准名包含原始列名
            elif standard_cn in col:# 只允许标准名被原始列名包含，不允许原始列名被标准名包含。否则会出现映射结果完全颠倒
                rename_map[col] = standard_en
                break

    # 重命名
    df_renamed = df.rename(columns=rename_map)

    # 如果需要只保留标准列
    if keep_only_standard:
        # 只保留标准英文列
        standard_cols = list(STANDARD_COLUMNS.values())
        cols_to_keep = []
        for col in standard_cols:
            if col in df_renamed.columns:
                cols_to_keep.append(col)

        df_clean = df_renamed[cols_to_keep].copy()
    else:
        df_clean = df_renamed.copy()

    # 补全缺失的标准列
    for col_en in standard_cols:
        if col_en not in df_clean.columns:
            df_clean[col_en] = pd.NA

    # 按标准顺序排列
    final_cols = []
    for col in standard_cols:
        if col in df_clean.columns:
            final_cols.append(col)
    if not keep_only_standard:
        extra_cols = []
        for col in df_clean.columns:
            if col not in standard_cols:
                extra_cols.append(col)
        final_cols = final_cols + extra_cols

    df_final = df_clean[final_cols].copy()

    print(f"原始列数: {len(df.columns)}")
    print(f"识别并重命名: {len(rename_map)} 列")
    print(f"保留列: {list(df_final.columns)}")
    return df_final

def save_to_csv(df: pd.DataFrame, filename: str, output_dir: str = None):
    '''
     将 DataFrame 保存到 data 目录（或指定目录）
    :param df: DataFrame
    :param filename: 文件名
    :param output_dir: 输出目录。默认 None 时保存到当前文件所在目录
    '''
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    # 确保目录在，不在则自动创建
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index = False,encoding = 'utf-8-sig')
    print(f'数据已经保存到：{filepath}')

def fetch_and_save(stock_code: str, symbol: str = None, filename: str = None):
    '''
    直接执行获取，标准化以及保存
    '''
    raw = get_stock_financial_data(stock_code, symbol)

    raw['股票代码'] = str(stock_code).zfill(6)  # 直接输入stock_code会出现代码前的0全被消除，先强制为字符串并保持六位
    raw['股票简称'] = symbol if symbol else stock_code

    clean = standardize_columns(raw)

    if filename is None:
        filename = f'{stock_code}_financial.csv'

    save_to_csv(clean, filename)
    return clean

if __name__ == '__main__':
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