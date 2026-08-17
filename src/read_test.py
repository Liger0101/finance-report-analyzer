import pandas as pd
import sys
sys.path.insert(0,r'D:/Project/libs')


# 使用csv文件时
df = pd.read_csv('D:/Project/finance-report-analyzer/data/ai_chip_market.csv')
print(df.head())

# 使用pdf文件时
import pdfplumber
with pdfplumber.open('D:/Project/finance-report-analyzer/data/京东工业：2025 年度报告.pdf') as pdf:
    pages = pdf.pages[0]
    print(pages.extract_text()[:500])
