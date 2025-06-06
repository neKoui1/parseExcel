from openai import AzureOpenAI
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')
AZURE_AI_41_KEY=config['Azure']['AZURE_AI_41_KEY']
AZURE_AI_41_ENDPOINT=config['Azure']['AZURE_AI_41_ENDPOINT']
print(AZURE_AI_41_KEY)
print(AZURE_AI_41_ENDPOINT)

client = AzureOpenAI(
    azure_endpoint=AZURE_AI_41_ENDPOINT,
    api_key=AZURE_AI_41_KEY,
    api_version='2025-03-01-preview'
)

response = client.chat.completions.create(
    model='o3',
    messages=[
        {
            'role':'user',
            'content':
            f'''
            回答以下问题：
            1. gpt o3模型和gpt-4o模型是一样的吗？为什么会叫o3和4o？
            2. o3模型使用的编码方式是什么？gpt4.1模型使用的编码方式是什么？
            3. o3模型和gpt4.1一次性能够对话的最大token是多少？
            4. 目前Azure OpenAI对中国大陆用户的定价是多少美元每百万token？
            5. 我该如何使用python来计算o3模型input有多少token？我需要计算的是python读取json文件后获得的dict类型。
            6. 输入的dict转为json_str后token总数约为44088521，我需要对输入进行一定的分割，按照100k的大小按顺序将
            转化后的文本输入给模型。输入的数据内容大致为
            会话id:[{"客服:"+"客服说的内容"}, {"客户:"+"客户说的内容"}]
            7. 针对数量级千万级别的token，在按照100ktoken的数据来分块之后，
            我该如何编写python代码在和ai的同一次会话中将这些内容分块输入？之后将最后的输出保存到md文件当中。
            注意：分块的目的就是能够将信息批量输入给和ai建立的同一段会话。假设使用模型的最大input token为120k
            针对上述问题，都给出具体的python代码演示
            '''
        },
    ])
output = response.choices[0].message.content
print(output)