import os

# 设置根目录（计算机科学期刊语料）
root_dir = '/Users/fafaya/Research-on-AI-generated-text-series/语料库/计算机科学期刊'

# 设置输出路径（保存到桌面）
desktop = '/Users/fafaya/Desktop'
output_path = os.path.join(desktop, 'Merge_all_abstracts_CS_cleaned.txt')

# 函数：清除非 ASCII 字符
def clean_text(text):
    return ''.join([c if ord(c) < 128 else ' ' for c in text])

# 收集摘要
all_abstracts = []
for journal_folder in os.listdir(root_dir):
    journal_path = os.path.join(root_dir, journal_folder)
    if os.path.isdir(journal_path):
        for filename in os.listdir(journal_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(journal_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        all_abstracts.append(content)
                except Exception as e:
                    print(f"❌ 无法读取文件 {file_path}，错误：{e}")

# 合并 + 清洗
merged_text = "\n\n".join(all_abstracts)
cleaned_text = clean_text(merged_text)

# 保存结果
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(cleaned_text)

print(f"✅ 成功汇总并清理 {len(all_abstracts)} 个摘要，已保存至：{output_path}")
