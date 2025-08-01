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
                你是花嫁丽舍的客服分析员，你现在要仔细研究邀约客服的微信聊天记录，也有一些宝宝宴跟内部对话，也要分析。
                全国一共7家分店。客服的首要目的，是要让客人进店参观，这也是需要你分析的点，你要做的，是发现客服遇到问题，
                比如：客人接触之后直接邀约成功的占比多少，话术好的地方，有问题的地方。针对类似问题，不同回答的成功率。
                类似问题，不同回答的沉默率。

                请严格按照以下json格式：
                案例x：“大概背景”，(x为当前数据分析的第几个对话，如案例1，案例2)
                好的地方：说明：“内容”，对话案例：“内容”（越详细越好）
                不好的地方：说明：“内容”，对话案例：“内容”（越详细越好）
                该单的状态：“”（失败，成功，或者其他你能说的）
                附属说明：“你能发现的别的问题，或者新发现”

                请提供可能多的案例给我，如果一个案例比较plain，not much to say 则可以忽略。对话案例要尽可能的详细。
                
                需要你分析的数据为{chunk}
                '''
            }
        ]
    )
    output = response.choices[0].message.content
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f'./model_output/8chunks_{idx+1}.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output)
        print(f'文件{idx+1}保存成功')


