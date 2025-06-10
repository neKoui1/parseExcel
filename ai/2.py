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
                你是上海花嫁丽舍婚礼中心的预约客服聊天研究员，你的任务是think hard，
                然后给公司的管理人员提供一份非常有价值的，基于聊天记录的非常详细的长报告。
                一定不能杜撰跟编造，任何总结一定要有举例。
                根据这些对话记录里做一些对于客户的画像的统计，找到客服与客户交流的渠道维度（相当于大方向小组维度），
                找到一些客户的特征，分析客户属性。以及关键节点的话语，让客户的态度改变的关键话语，
                或者是客户最关心的地方，目的是要让管理人员发现很多平时不能发现的问题。
                注意这些是已经总结好的聊天记录，上下文不完整且语音或者电话沟通内容并不在里面，you should take consideration.
                客服的目的是先跟客人沟通，然后最后邀约进店参观就算是完成任务，
                所以你的关注点，要在邀约进店之前，就是什么关键因素让人答应邀约进店，
                内部聊天也可以关注，给我更多的定量数据。
                找到相同问题什么样的回复会让客户接受率比较高的能够聊下去，而不是导致客户失联。
                找到客户愿意聊下去的时间节点，客服在交流时跟进了几次（使用了什么活动或者话术）邀约的成功率更高，以及客户反感的点是什么。
                比较一下客人针对客服发放的物料部分（门头/厅介绍/婚纱场馆等）看到哪一部分更加感兴趣？更愿意互动？
                在加上客户好友之后，客服交流后不愿意说话的客户占比多少？你应该优先分析说话的客户。
                你也要总结一下组内各人员客服的沟通情况。例如：
                1.客服遇到问题，比如：拿到客资之后直接邀约成功的占比多少，话术好的地方，有问题的地方
                2.加上微信后客户提及比较多的问题，A客服回复和B客服回复后的成功率
                可以给我更多的例子，更多管理层可能忽略的痛点（这个最重要），顾客关心的问题，定量的客户画像分析。
                在统计方面可以有一些数据比如：指标，客群结构，宴会类型占比，客户画像（画像标签，占比，典型诉求，例证），桌数区间（e.g.< 8桌   % 桌   % ｜ >  桌   %，极大单：桌出现 ？ 次；极小单：出现 ？次）），客户关注焦点（详细一些），关键话语 & 情绪转折，（包括正向触发，以及负向触发，尽量详细要有统计），管理层要关心的痛点（要有案例跟影响结果），内部管理优化的点（要有例子）别的方面你需要根据给到的数据，自己再去归纳出一些数据层面。
                最后，你应该输出跟竞品对比时我们的优势和不足，你在比较时需要给出相关竞品的名字以及竞品所拥有的优势。
                不需要输出任何建议，可以有一个章节专门说一些有趣的finding（这个也是多多益善），还有管理层会对之感兴趣，不易被发现的点。
                
                需要你分析的数据为{chunk}
                '''
            }
        ]
    )
    output = response.choices[0].message.content
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f'./model_output/o3_{idx+1}.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output)
        print(f'文件{idx+1}保存成功')


