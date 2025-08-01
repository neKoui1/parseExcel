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

with open('./model_output/output.md', 'r', encoding='utf-8') as f:
    content = f.read()
    print('读取文件成功')

client=AzureOpenAI(
    azure_endpoint=AZURE_AI_41_ENDPOINT,
    api_key=AZURE_AI_41_KEY,
    api_version='2025-04-01-preview',
)


enc = tiktoken.get_encoding('cl100k_base')
tokens = enc.encode(content)
max_tokens=200_000
tokens_count=len(tokens)
chunks=[]
print(f'tokens_count={tokens_count}')
start=0
while start<tokens_count:
    end=min(start+max_tokens,tokens_count)
    chunk_tokens=tokens[start:end]
    chunk_str=enc.decode(chunk_tokens)
    chunks.append(chunk_str)
    start=end
print(f'分成了{len(chunks)}段，每段最大 {max_tokens} tokens')

for idx, chunk in enumerate(chunks):
    output=''
    print(f'对第{idx+1}块chunk进行对话处理')
    response = client.chat.completions.create(
        model='o3',
        messages=[
            {
                'role':'user',
                'content': 
                f'''
                你是花嫁丽舍的客服分析员，你现在要仔细研究邀约客服的微信聊天记录，也有一些宝宝宴跟一些内部对话，也要分析。全国一共7家分店。你要做的，是仔细查看每条对话里体现的，竞品对比我们（花嫁丽舍）的优势和不足，提及竞品比较多的名字，及提及竞品的优势，并给出案例。要尽量详细，案例越多越好，禁止杜撰。
                请严格按照以下json格式：
                背景：""（对话的背景）
                竞品：""（竞品名称）
                我们的优势："1. (优势1) 2. （优势2） ..."
                我们的不足："1. (不足1) 2. （不足2） ..."
                竞品的特点:""
                聊天案例："客户：（客户说的内容） 客服：（客服说的内容）"（聊天截取）
                需要你分析的数据为{chunk}。pay attention: 输出的json格式应完全符合上述要求格式，包括标点符号
                '''
            }
        ]
    )
    output = response.choices[0].message.content
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f'./model_output/竞品分析prompt8_{idx+1}.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output)
        print(f'文件{idx+1}保存成功')


