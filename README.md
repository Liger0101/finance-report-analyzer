# 财报分析器(Finance Report Analyzer)

## 项目简介

本项目是一个基于 Python 和 LLM 的财报分析工具，能够自动获取财报文件并读取财报文件，自动提取关键财务指标，并生成自然语言分析报   告

## 功能列表

- **自动获取数据**：基于 Akshare 获取上市公司财务指标
- **列名标准化**：自动识别中英文列名，统一为标准英文列名
- **中文单位转换**：自动将「万」「亿」「%」等转为纯数字
- **衍生指标计算**：补全销售净利率，计算净利润现金比
- **指标字典生成**：提取最新一期数据，生成结构化字典
- **AI 报告生成**：调用 DeepSeek API 生成财务分析报告
- **批量处理**：支持单个、批量、处理已有文件三种模式

## 技术栈

- **语言**：Python 3.12
- **数据获取**：Akshare
- **数据处理**：Pandas, Numpy
- **文件格式**：CSV(utf-8-sig)，Markdown
- **LLM**: DeepSeek API（openai SDK）

## 目录结构

```txt
finance-report-analyzer/
├── data/ # 财务数据存放目录
│ ├── data_fetcher.py # 数据获取与标准化模块
│ └── *.csv # 标准化后的财务数据
├── src/ # 源代码目录
│ ├── data_processor.py # 数据处理与指标生成模块
│ ├──  llm_reporter.py # LLM 报告生成模块
│ └── main.py # 主程序入口
├── output/ # 输出目录
│ └── *.md # 财务分析报告
├── README.md
└── requirements.txt
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置Deepseek API Key
1. 访问 platform.deepseek.com，注册并创建 API Key。
2. 设置环境变量，在Windows PowerShell中，输入setx DEEPSEEK_API_KEY "你的key"
3. 重启Pycharm

## 使用方法
1. 使用主程序
2. 运行各个模块

## 字段说明
- 英文字段——中文字段——单位
- stock_code——股票代码——无
- stock_name——股票简称——无
- report_date——报告期——无
- revenue——营业总收入——元
- revenue_yoy——营收同比增长率——元
- net_profit——净利润——元
- net_profit_yoy——净利润同比增长率——元
- gross_margin——销售毛利率——%
- net_margin——销售净利率——%
- roe——净资产收益率——%
- debt_ratio——资产负债率——%
- bvps——每股净资产——元
- ocf_ps——每股经营现金流——元
- eps——基本每股收益——元
- profit_cash_ratio——净利润现金比——无

## 后续规划
- 补充更多财务指标计算
- 增加报告历史对比功能
- 接入更多数据源

## 已知问题
- 由于Akshare数据源的限制，revenue数据可能缺失
- 对于模糊匹配部分，列名相似时可能导致数据误匹配
- 部分股票代码前导是0，目前已用 zfill(6) 处理，但需全程保持字符串

## 效果展示
![演示](https://raw.githubusercontent.com/Liger0101/finance-report-analyzer/main/docs/demo.gif)