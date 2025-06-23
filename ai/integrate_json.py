import configparser
from openai import AzureOpenAI
import json
import tiktoken
from datetime import datetime
import os

config = configparser.ConfigParser()
config.read('./config.ini')

AZURE_AI_41_KEY = config['Azure']['AZURE_AI_41_KEY']
AZURE_AI_41_ENDPOINT = config['Azure']['AZURE_AI_41_ENDPOINT']

def load_json_files():
    """读取所有JSON文件"""
    json_data = []
    for filename in os.listdir('./model_output'):
        if filename.endswith('.json'):
            with open(f'./model_output/{filename}', 'r', encoding='utf-8') as f:
                data = json.load(f)
                json_data.append({'filename': filename, 'data': data})
    return json_data

def create_prompt(json_data):
    """创建整合prompt"""
    return f'''
你是花嫁丽舍的客服数据分析专家，需要整合所有JSON文件中的案例数据。

【核心要求】
1. 绝对不允许遗漏任何数据
2. 保持原始数据完整性
3. 按统一JSON格式输出
4. 案例编号连续递增

【输出格式】
{{
  "案例X": "背景描述",
  "好的地方": {{
    "说明": "分析内容",
    "对话案例": ["对话1", "对话2"]
  }},
  "不好的地方": {{
    "说明": "分析内容", 
    "对话案例": ["对话1", "对话2"]
  }},
  "该单的状态": "状态",
  "附属说明": "额外发现"
}}

【待整合数据】
{json.dumps(json_data, ensure_ascii=False, indent=2)}

请完整整合所有案例，确保无遗漏。
'''

def main():
    # 读取JSON文件
    json_files = load_json_files()
    print(f"读取到 {len(json_files)} 个JSON文件")
    
    # 创建客户端
    client = AzureOpenAI(
        azure_endpoint=AZURE_AI_41_ENDPOINT,
        api_key=AZURE_AI_41_KEY,
        api_version='2025-04-01-preview',
    )
    
    # 生成prompt
    prompt = create_prompt(json_files)
    
    # 调用API
    response = client.chat.completions.create(
        model='o3',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.1
    )
    
    # 保存结果
    output = response.choices[0].message.content
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(f'./model_output/integrated_{timestamp}.json', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"整合完成，保存为: integrated_{timestamp}.json")

if __name__ == "__main__":
    main() 