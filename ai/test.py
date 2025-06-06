import json
import random
from datetime import datetime
import tiktoken

def count_tokens(input_dict, model_name='o3') -> int:
    if 'gpt-4' in model_name or 'gpt-3.5-turbo' in model_name:
        encoding = tiktoken.encoding_for_model(model_name)
    else:
        encoding = tiktoken.get_encoding('cl100k_base')
    json_str = json.dumps(input_dict, ensure_ascii=False)
    token_count = len(encoding.encode(json_str))
    return token_count

encoding=tiktoken.get_encoding('cl100k_base')
max_tokens=100_000

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

with open('./model_output/o4mini_model_output_2025-06-06_17-39-13.md', 'r', encoding='UTF-8') as f:
    content = f.read()
print(type(content))
enc = tiktoken.get_encoding('cl100k_base')
tokens = enc.encode(content)
token_count = len(tokens)
print(f'output_token_count={token_count}')

