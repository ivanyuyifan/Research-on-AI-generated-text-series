# 设置文件路径
file_path = '/Users/fafaya/Research-on-AI-generated-text-series/Abstracts_Corpus_All(Linguisitcs)/Merge_all_abstracts.txt'

# 读取并统计词数
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()
    word_count = len(text.split())

print(f"🔢 该文件总词数为：{word_count}")
