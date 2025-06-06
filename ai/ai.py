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
# print(AZURE_AI_41_KEY)
# print(AZURE_AI_41_ENDPOINT)

with open('./output/output_202505260253.json', 'r', encoding='UTF-8') as f:
    content = json.load(f)
json_str = json.dumps(content, ensure_ascii=False)
enc = tiktoken.get_encoding('cl100k_base')
tokens = enc.encode(json_str)
max_tokens=100_000
# chunk_tokens=tokens[max_tokens*30:max_tokens*31]
# chunk_str=enc.decode(chunk_tokens)
# print(f'{chunk_str}')


client=AzureOpenAI(
    azure_endpoint=AZURE_AI_41_ENDPOINT,
    api_key=AZURE_AI_41_KEY,
    api_version='2025-03-01-preview',
)

def chunk_by_tokens(json_str, max_tokens=100_000):
    enc=tiktoken.get_encoding('cl100k_base')
    tokens=enc.encode(json_str)
    tokens_count=len(tokens)
    print(f'tokens_count={tokens_count}')
    chunks=[]
    start=0
    while start<tokens_count:
        end=min(start+max_tokens, tokens_count)
        chunk_tokens=tokens[start:end]
        chunk_str=enc.decode(chunk_tokens)
        chunks.append(chunk_str)
        start=end
    print(f'分成了{len(chunks)}段，每段最大 {max_tokens} tokens')
    return chunks

chunks=chunk_by_tokens(json_str, max_tokens)

time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_path = f'./model_output/o4mini_model_output_{time_stamp}.md'

for idx, chunk in enumerate(chunks):
    user_msg=f'第{idx+1}块内容: '      
    response=client.chat.completions.create(
        model='o4-mini',
        messages=[
            {
                'role': 'user',
                'content': 
                f'''
                你是上海花嫁丽舍婚礼中心的预约客服聊天研究员，你的任务是仔细查看所有的聊天记录，并且把每一组对话都进行详细概括，并给出1-2个例子。
                我只需要json，不需要其他的任何信息。
                要求输出json格式:
                id,
                概括，
                例子（要求一定要有代表性，或者有冲突性，2-3组对话，客户的话语优先选中，必要时可以适当增加），要尽量详细
                状态：成功，失败，待定，或者其他你能概括的
                其他信息：你能发现的有趣/有必要的信息都放在这里，尽量详细
                门店信息：上海或者北京，或者未知
                客户画像：新娘，新郎，爸妈，或者你自己去根据聊天信息判断，若不能判断就未知，也可对画像的喜好，或者财富程度做一个评价，要尽量详细。
                桌数：对于桌数的要求

                注意：如果是内部聊天，也可以做一个对于内部聊天内容的概括跟必要信息，其他还有宝宝宴什么的也可以记录
                本次需要分析的聊天记录为{chunk}
                '''
            },
        ],
    )
    output = response.choices[0].message.content
    with open(file_path, 'a', encoding='UTF-8') as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write(user_msg+'\n')
        f.write(output)
        print(f'第{idx+1}个chunk已保存成功')
        f.write("\n" + "=" * 50 + "\n")

print(f'所有chunk均打印成功')





# response = client.chat.completions.create(
#     model='o4-mini',
#     messages=[
#         {
#             "role":"user",
#             "content":
#             f'''
#             你是上海花嫁丽舍婚礼中心的预约客服聊天研究员，你的任务是仔细查看所有的聊天记录，并且把每一组对话都进行详细概括，并给出1-2个例子。
#             我只需要json，不需要其他的任何信息。
#             要求输出json格式:
#             id,
#             概括，
#             例子（要求一定要有代表性，或者有冲突性，2-3组对话，客户的话语优先选中，必要时可以适当增加），要尽量详细
#             状态：成功，失败，待定，或者其他你能概括的
#             其他信息：你能发现的有趣/有必要的信息都放在这里，尽量详细
#             门店信息：上海或者北京，或者未知
#             客户画像：新娘，新郎，爸妈，或者你自己去根据聊天信息判断，若不能判断就未知，也可对画像的喜好，或者财富程度做一个评价，要尽量详细。
#             桌数：对于桌数的要求

#             注意：如果是内部聊天，也可以做一个对于内部聊天内容的概括跟必要信息，其他还有宝宝宴什么的也可以记录
#             本次需要分析的聊天记录为{chunk_str}
#             '''
#         },
#     ],
# )
# output = response.choices[0].message.content
# print('本次会话的output为{output}'.format(output=output), sep='\n')

# time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# file_path = f'./model_output/o4mini_model_output_{time_stamp}.md'
# with open(file_path, 'w', encoding='UTF-8') as f:
#     f.write(output)
# print('markdown文件已保存成功')

# client = OpenAI(api_key=APIKEY, base_url=BASEURL)

# output=''
# for key, val in content.items():
#     response = client.chat.completions.create(
#         model='deepseek-chat',
#         messages=[
#             {
#                 'role':'user',
#                 'content': 
#                 '''你现在是一位根据婚恋市场客服与客户聊天内容进行分析的数据分析专家，
#                 在此过程中，你应该根据客服与该会话id的用户的聊天内容提取出客户画像、客服质量和交易的痛点。
#                 在客户画像中，你应该提取到该用户的客资来源、预算分层和最常询问的主题（如价格、场地、档期等）。
#                 在客服质量中，你应该提取并计算出负面情绪的占比，并对客服的互怼或者脏话场景进行标记。
#                 在交易痛点中，你应该提取出交易失败的原因，如重复客资装单、价位太高导致客户流失、权限/表单堵塞等。
#                 你每一次输出的结果都将会和下一个会话id的聊天记录一起提交给你，你需要保留并根据下一个会话id更新这些output.
#                 下面我将输入会话id和对应的聊天内容，请你开始分析'''+ "会话id: {key}, 聊天内容为: {val}".format(key=key, val=val)
#                 + "上一次对话的结果为{output}".format(output=output)
#             }
#         ]
#     )
#     output = response.choices[0].message.content
#     print('会话{key}的output为{output}'.format(key=key, output=output), sep='\n')

# print(output)