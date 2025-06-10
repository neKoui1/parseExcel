from openai import AzureOpenAI
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

AZURE_AI_41_KEY=config['Azure']['AZURE_AI_41_KEY']
AZURE_AI_41_ENDPOINT=config['Azure']['AZURE_AI_41_ENDPOINT']

file_paths=[]
for i in range(1,9):
    file_paths.append(f'./model_output/o3_{i}.md')

contents=[]
for _, v in enumerate(file_paths):
    with open(v, 'r', encoding='utf-8') as f:
        contents.append(f.read())

client=AzureOpenAI(
    azure_endpoint=AZURE_AI_41_ENDPOINT,
    api_key=AZURE_AI_41_KEY,
    api_version='2025-04-01-preview',
)

response=client.chat.completions.create(
    model='o3',
    messages=[
        {
            'role':'user',
            'content':
            f'''
            你是上海花嫁丽舍婚礼中心的预约客服聊天研究员，你现在的任务是综合八篇聊天记录报告，写出一篇综合所有报告内容的大报告。
            注意：
            - 把所有的统计数据，严格的合并，不要省去任何例子。
            - 合并总结所有的内容，你需要的是合并而不是省去。
            总之，相当于把这八篇报告合并在一起，但是要结构上变成一篇报告且不省去任何内容。报告越详细越好。
            输入的内容为
            {contents[0]},
            {contents[1]},
            {contents[2]},
            {contents[3]},
            {contents[4]},
            {contents[5]},
            {contents[6]},
            {contents[7]}
            '''
        }
    ]
)
output=response.choices[0].message.content
with open('./model_output/o3_result.md', 'w', encoding='utf-8') as f:
    f.write(output)
    print('文件保存成功')

