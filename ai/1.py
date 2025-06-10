import tiktoken
with open('./model_output/output.md', 'r', encoding='utf-8') as f:
    c = f.read()
enc = tiktoken.get_encoding('cl100k_base')
tokens = enc.encode(c)
print(f'token_count = {len(tokens)}')