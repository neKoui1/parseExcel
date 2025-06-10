import re
import tiktoken

def remove_specific_blocks(md_file_path, output_file_path=None):
    if output_file_path is None:
        output_file_path=md_file_path
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r'=+\s*\n=+\s*\n第\d+块内容[：:]\s*\n'
    cleaned_content=re.sub(pattern, '', content)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)


md_file_path='./model_output/o4mini_model_output_2025-06-06_17-39-13.md'
output_file_path='./model_output/output.md'
remove_specific_blocks(md_file_path=md_file_path, output_file_path=output_file_path)
print("替换成功")