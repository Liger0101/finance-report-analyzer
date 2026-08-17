"""
财报数据处理模块
读取、清洗、计算财务指标
"""

import pandas as pd
import numpy as np
import os   # 操作文件路径、创建文件夹、读取环境变量、执行系统命令等。
import glob #  按模式查找文件路径。

def load_financial_data(filepath: str) -> pd.DataFrame:
    """
    读取 CSV 财报数据
    """
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    print(f"读取文件: {filepath}")
    print(f"数据形状: {df.shape}")
    return df



if __name__ == "__main__":
    load_financial_data('D:/Project/finance-report-analyzer/data/万科A_financial.csv')