from openai import AzureOpenAI
import json
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

AZURE_AI_41_KEY=config['Azure']['AZURE_AI_41_KEY']
AZURE_AI_41_ENDPOINT=config['Azure']['AZURE_AI_41_ENDPOINT']

file_paths=[]
for i in range(1,9):
    file_paths.append(f'./model_output/8chunks_{i}.json')

contents=[]
for _, v in enumerate(file_paths):
    with open(v, 'r', encoding='utf-8') as f:
        data = json.load(f)
        contents.append(data)

client=AzureOpenAI(
    azure_endpoint=AZURE_AI_41_ENDPOINT,
    api_key=AZURE_AI_41_KEY,
    api_version='2025-04-01-preview',
)

for i in range(8):
    response=client.chat.completions.create(
        model='o3',
        messages=[
            {
                'role':'user',
                'content':
                f'''
                你是上海花嫁丽舍婚礼中心的预约客服聊天研究员，你的任务是根据这8篇报告里的所有JSON数据整合并且生成一个直观的，符合JSON格式类似excel表格的HTML网页。
                这是第{i+1}次输入，本次输入的内容为：
                {contents[i]},
                注意：
                - 不同输入里的报告写的形如“样例1”的格式都是各自独立的，不允许覆盖掉，每一个都需要分析。
                - 所有的原数据都应该能在输出结果中呈现出来，保持所有的原数据不变并且按照JSON数据格式直观生成HTML的报表。
                - 整合所有的JSON内容生成一个报表，所有的数据都应该能在HTML文件中找到，pay attention: 不允许任何省略！
                - 除了上面两个要求以外你不应该做任何多余的分析、返回多余的语句。
                总之，相当于把这八篇报告所有内容合并在一起的HTML文件，但是要结构上变成一篇直观的报表，不允许因为数据量的问题而省略输出！
                '''
            }
        ]
    )
    output=response.choices[0].message.content
    with open('./model_output/8chunks_result.html', 'a', encoding='utf-8') as f:
        f.write(output)
        print('文件保存成功')

