'''
财报数据获取模块
利用akshare获取上市公司的财务模块，并标准化列标签
'''

import pandas as pd
import akshare as ak
import os

#1.定义标签列表
STANDARD_COLUMNS = {
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
    模糊匹配 + 标准化列名 + 补全缺失列

    参数:
        df: 原始 DataFrame
        keep_only_standard: 是否只保留 STANDARD_COLUMNS 中定义的列
                           True  -> 只保留标准列（默认）
                           False -> 保留原始所有列，但重命名能识别的列
    """
    # 1. 去掉列名里的空格和换行（Akshare 经常有奇怪空白）
    df.columns = [str(c).replace('\n', '').replace('\r', '').strip() for c in df.columns]

    # 2. 建立反向映射：原始名 -> 标准英文名
    rename_map = {}
    for standard_cn, standard_en in STANDARD_COLUMNS.items():
        for col in df.columns:
            # 完全匹配
            if col == standard_cn:
                rename_map[col] = standard_en
                break
            # 模糊匹配：原始列名包含标准名 或 标准名包含原始列名
            elif standard_cn in col or col in standard_cn:
                rename_map[col] = standard_en
                break

    # 3. 执行重命名
    df_renamed = df.rename(columns=rename_map)

    # 4. 如果需要只保留标准列
    if keep_only_standard:
        # 只保留标准英文列
        standard_cols = list(STANDARD_COLUMNS.values())
        cols_to_keep = [c for c in standard_cols if c in df_renamed.columns]
        df_clean = df_renamed[cols_to_keep].copy()
    else:
        df_clean = df_renamed.copy()

    # 5. 补全缺失的标准列（值为 NaN）
    for col_en in standard_cols:
        if col_en not in df_clean.columns:
            df_clean[col_en] = pd.NA

    # 6. 按标准顺序排列
    final_cols = [c for c in standard_cols if c in df_clean.columns]
    if not keep_only_standard:
        extra_cols = [c for c in df_clean.columns if c not in standard_cols]
        final_cols = final_cols + extra_cols

    df_final = df_clean[final_cols].copy()

    print(f"原始列数: {len(df.columns)}")
    print(f"识别并重命名: {len(rename_map)} 列")
    print(f"保留列: {list(df_final.columns)}")
    return df_final

def save_to_csv(df: pd.DataFrame, filename: str, output_dir: str = None):
    '''
    保留dataFrame到data目录中
    '''
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index = False,encoding = 'utf-8')
    print(f'数据已经保存到：{filepath}')

def fetch_and_save(stock_code: str, symbol: str = None, filename: str = None):
    '''
    直接执行获取，标准化以及保存
    '''
    raw = get_stock_financial_data(stock_code, symbol)
    clean = standardize_columns(raw)

    if filename is None:
        filename = f'{stock_code}_finance.csv'

    save_to_csv(clean, filename)
    return clean

if __name__ == '__main__':
    df = fetch_and_save(stock_code="600519",symbol="贵州茅台",filename="maotai_financial.csv")
    print('数据预览：\n')
    print(df.head())