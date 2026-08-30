# -*- coding: utf-8 -*-
"""
LLM 分析报告生成模块
"""

import os
from datetime import datetime
from openai import OpenAI

def load_api_key() -> str:
    """
    从环境变量读取 DeepSeek API Key
    在之前先在终端设置：setx DEEPSEEK_API_KEY "key"
    """
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError('未找到 DEEPSEEK_API_KEY，请先设置环境变量')
    return api_key

def build_prompt(indicator_dict: dict) -> str:
    """把指标字典拼接成分析提示词"""
    company = indicator_dict.get('company_name','未知公司')
    code = indicator_dict.get('stock_code','')
    report_date = indicator_dict.get('report_date','')

    prompt = f"""
你是一位专业的金融分析师。请根据以下财务数据，用中文生成一份简洁的财务分析报告。

## 公司基本信息
- 公司名称：{company}
- 股票代码：{code}
- 报告期：{report_date}

## 核心财务指标
- 销售毛利率：{indicator_dict.get('gross_margin', 'N/A')}%
- 销售净利率：{indicator_dict.get('net_margin', 'N/A')}%
- 净资产收益率（ROE）：{indicator_dict.get('roe', 'N/A')}%
- 资产负债率：{indicator_dict.get('debt_ratio', 'N/A')}%
- 每股净资产（BVPS）：{indicator_dict.get('bvps', 'N/A')} 元
- 每股经营现金流（OCF/PS）：{indicator_dict.get('ocf_ps', 'N/A')} 元
- 基本每股收益（EPS）：{indicator_dict.get('eps', 'N/A')} 元
- 净利润现金比：{indicator_dict.get('profit_cash_ratio', 'N/A')}

## 报告要求
请按以下结构输出，总字数控制在300字以内：

1. **盈利能力分析**（2-3句）
2. **财务健康分析**（2-3句）
3. **利润质量分析**（2-3句）
4. **综合评价**（1-2句，给出评级：优秀/良好/一般/关注）

直接输出报告内容，不要输出任何其他说明文字。
"""
    return prompt


def generate_report(indicator_dict: dict) -> str:
    """调用 LLM 生成分析报告"""
    api_key = load_api_key()

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    prompt = build_prompt(indicator_dict)

    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位专业的金融分析师，擅长用简洁的语言解读财务数据。"},
            {"role": "user", "content": prompt},
        ],
        temperature = 0.7,
        max_tokens = 800
    )

    report_text = response.choices[0].message.content
    return report_text


def save_report(indicator_dict : dict, report_text: str) -> str:
    """
    保存报告到 output 目录
    """
    # 从字典中取公司名，缺失时用"未知公司"
    company_name = str(indicator_dict.get('company_name', '未知公司'))

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, 'output')
    os.makedirs(output_dir,exist_ok=True)

    today = datetime.now().strftime('%Y%m%d')
    filename = f'{company_name}_分析报告_{today}.md'
    file_path = os.path.join(output_dir, filename)

    with open(file_path, 'w', encoding = 'utf-8-sig') as f:
        f.write(f"# {company_name} 财务分析报告\n\n")
        f.write(f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(report_text)

    print(f'报告已保存至：{file_path}')
    return file_path

if __name__ == "__main__":
    # 测试：用模拟数据跑通
    test_data = {
        "company_name": "贵州茅台",
        "stock_code": "600519",
        "report_date": "2026-06-30",
        "gross_margin": 89.56,
        "net_margin": 50.75,
        "roe": 16.75,
        "debt_ratio": 15.19,
        "profit_cash_ratio": 1.59,
        "eps": 35.57,
        "bvps": 200.99,
    }
    report = generate_report(test_data)
    print("\n生成的报告：\n")
    print(report)

    save_report(test_data, report)