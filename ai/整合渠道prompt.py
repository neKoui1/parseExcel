import configparser
from openai import AzureOpenAI
import json
import tiktoken
from datetime import datetime

config = configparser.ConfigParser()
config.read('./config.ini')

AZURE_AI_41_KEY=config['Azure']['AZURE_AI_41_KEY']
AZURE_AI_41_ENDPOINT=config['Azure']['AZURE_AI_41_ENDPOINT']

content=list()
for i in range(1,9):
    with open(f'./model_output/渠道prompt8_{i}.json','r', encoding='utf-8') as f:
        data = json.load(f)
        content.append(data)

client=AzureOpenAI(
    azure_endpoint=AZURE_AI_41_ENDPOINT,
    api_key=AZURE_AI_41_KEY,
    api_version='2025-04-01-preview',
)

response = client.chat.completions.create(
    model='o3',
    messages=[
        {
            'role':'user',
            'content':
            f'''
            你现在需要整合所有JSON文件中的案例数据。

            【核心要求】
            1. 绝对不允许遗漏任何数据 - 每个案例中的内容都必须被包含
            2. 保持原始数据的完整性和准确性
            3. 按照统一的JSON格式输出
            4. 对话案例要尽可能详细，包含完整的上下文
            5. 你需要考虑将相同的类别合并在一起

            【输出格式要求】
            请严格按照以下json格式输出，输出内容只包括以下一条json的内容：
            渠道：
                - 占比
                - 占比
                - 占比

            客户人员：
                -”“（新娘，新郎，父母，或者其他你能发现的）占比
                -占比
                -占比

            客户喜好：
                -”“ 占比
                -占比
                -占比

            客户属性：（比如中产，省钱达人，有钱人等等）
                -占比
                -占比
                -占比
            竞品占比:（客户在对话中提到的其他店的占比）
                -占比
                -占比
            
            【数据完整性检查】
            - 确保每个输入文件中的案例都被包含
            - 确保对话案例的完整性
            - 确保分析内容的准确性

            【待整合的数据】
            {json.dumps(content,ensure_ascii=False,indent=2)}
            请完整整合所有案例，确保无遗漏。
            '''
        }
    ]
)

output = response.choices[0].message.content
with open(f'./model_output/渠道integrated.json', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'渠道整合完成')
