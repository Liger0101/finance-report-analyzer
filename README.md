# 财报分析器(Finance Report Analyzer)

## 项目简介

本项目是一个基于 Python 和 LLM 的财报分析工具，能够读取财报文件，自动提取关键财务指标，并生成自然语言分析报告

## 功能列表

- [ ] 读取财报文件
- [ ] 自动计算关键财务指标(ROE，毛利率，资产负债等)
- [ ] 调用 LLM 生成分析报告
- [ ] 支持多公司批量处理

## 技术栈

- Python
- Pandas
- Akshare
- LLM API

## 目录结构

```
finance-report-analyzer/
├── data/              # 存放财报文件
│   ├── data_fetcher.py    # 数据获取模块
│   ├── batch_fetch.py  # 示例数据获取
│   ├── 万科A_financial.csv   #示例数据
│   └── ...
├── src/               # 源代码
│   └── .gitkeep
├── output/            # 输出分析报告
│   └── .gitkeep
├── README.md          # 项目说明
└── requirements.txt   # 依赖列表
```

## 示例数据说明
当前 data 目录包含以下公司的财务数据：
- 贵州茅台-600519-白酒
- 招商银行-600036-银行
- 比亚迪-002594-新能源车
- 恒瑞医药-600276-医药
- 万科A-000002-地产