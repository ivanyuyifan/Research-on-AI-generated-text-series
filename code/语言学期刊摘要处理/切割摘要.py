import os
from nltk.tokenize import sent_tokenize

# 输入输出路径
input_path = "/Users/fafaya/Desktop/Merge_all_abstracts.txt"
output_dir = "/Users/fafaya/Desktop/Abstracts_Split"
os.makedirs(output_dir, exist_ok=True)

# 读取并按句切割
with open(input_path, 'r', encoding='utf-8') as f:
    text = f.read()

sentences = sent_tokenize(text)
chunk_size = 10  # 每 10 句为一个文件

print(f"📄 总句数: {len(sentences)}，将生成 {len(sentences)//chunk_size + 1} 个 chunk 文件...")

# 写入 chunk 文件
for i in range(0, len(sentences), chunk_size):
    chunk = ' '.join(sentences[i:i+chunk_size])
    filename = f"chunk_{i//chunk_size}.txt"
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f_out:
        f_out.write(chunk)

print(f"✅ 所有 chunk 文件已保存至: {output_dir}")
