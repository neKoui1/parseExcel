import json
import tiktoken
import random

with open('./output/output_202505260253.json', 'r', encoding='utf-8') as f:
    content_dict = json.load(f)
json_str = json.dumps(content_dict, ensure_ascii=False)
print(json_str)
enc = tiktoken.get_encoding('cl100k_base')
tokens = enc.encode(json_str)
max_tokens=100_000
# token_type = type(tokens)
token_count = len(tokens)
print(f'token_count={token_count}')
print(f'o3 token_cost={(token_count/100000)} dollar')
print(f'4.1 token_cost={(token_count/1000000)*2} dollar')


