# clean_text_mac.py

input_path = "/Users/fafaya/Desktop/Abstracts_All/Merge_all_abstracts.txt"
output_path = "/Users/fafaya/Desktop/Abstracts_All/Merge_all_abstracts_cleaned.txt"

def clean_text(text):
    # 把所有非 ASCII 字符替换成空格
    return ''.join([c if ord(c) < 128 else ' ' for c in text])

with open(input_path, 'r', encoding='utf-8') as f:
    text = f.read()

cleaned = clean_text(text)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(cleaned)

print("✅ 清理完成！生成文件：", output_path)
