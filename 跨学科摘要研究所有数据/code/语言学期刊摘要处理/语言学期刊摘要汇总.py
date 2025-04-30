import os

# 输入路径：所有干净的摘要 .txt 文件
input_folder = '/Users/fafaya/Desktop/AL_Abstracts_All'

# 输出路径：合并并清洗后的最终文件
output_path = '/Users/fafaya/Desktop/Merge_all_abstracts_AL_cleaned.txt'

# 清洗函数：仅保留 ASCII 字符（去除中文、特殊符号）
def clean_text(text):
    return ''.join([c if ord(c) < 128 else ' ' for c in text])

# 收集并清洗所有摘要
all_abstracts = []
for filename in sorted(os.listdir(input_folder)):
    if filename.endswith('.txt'):
        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as f:
            content = f.read().strip()
            cleaned = clean_text(content)
            all_abstracts.append(cleaned)

# 合并为一个文本块（用两个换行分隔）
merged_text = "\n\n".join(all_abstracts)

# 写入最终文件
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(merged_text)

print(f"✅ 成功合并并清洗 {len(all_abstracts)} 个摘要，文件保存至：{output_path}")
