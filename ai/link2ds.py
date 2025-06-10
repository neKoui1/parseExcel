import configparser
from openai import AzureOpenAI
import json
import tiktoken
from datetime import datetime

config = configparser.ConfigParser()
config.read('./config.ini')

BASEURL=config['DS']['BASEURL']
APIKEY=config['DS']['APIKEY']
AZURE_AI_41_KEY=config['Azure']['AZURE_AI_41_KEY']
AZURE_AI_41_ENDPOINT=config['Azure']['AZURE_AI_41_ENDPOINT']

with open('./model_output/o4mini_model_output_2025-06-06_17-39-13.md','r', encoding='utf-8') as f:
    md_content = f.read()

client=AzureOpenAI(
    azure_endpoint=AZURE_AI_41_ENDPOINT,
    api_key=AZURE_AI_41_KEY,
    api_version='2025-03-01-preview',
)

response = client.chat.completions.create(
    model='o4-mini',
    messages=[
        {
            'role':'user',
            'content':
            f'''
            我现在有一个在python中使用open函数打开的md文件需要处理。
            在这个md文件中，有的json格式用markdown的代码块符号语法包围起来，有的没有使用md代码块。
            注意：我需要你把形如“=========”的分隔符和“第x块内容”这些不是json的内容全部删除处理掉，
            仅仅保留所有的json相关的内容（不允许有任何json内容的信息流失！），
            之后我会将这些json按照md的代码块保存到markdown文件中，
            所以你输出的所有内容应该都只包括处理后的文件内容，而不应该包含例如“收到、好的”等LLM的常规回复，因为这会影响我的文件保存内容。
            输入的md文件的内容为{md_content}
            '''
        }
    ]
)

output = response.choices[0].message.content
print(output)

file_path = f'./model_output/output.md'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(output)

print('运行成功')