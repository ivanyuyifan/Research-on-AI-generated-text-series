import os

# 根目录路径
root_dir = '/Users/fafaya/Research-on-AI-generated-text-series/语料库/应用语言学期刊'

# 收集所有摘要内容
all_abstracts = []

# 遍历所有子文件夹
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.txt'):
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    all_abstracts.append(content)
            except Exception as e:
                print(f'无法读取文件 {file_path}，错误：{e}')

# 将所有摘要连接为一个大文本，中间用两个换行分隔
full_text = "\n\n".join(all_abstracts)

# 输出路径（你可以自定义名称）
output_txt_path = '/Users/fafaya/Research-on-AI-generated-text-series/语料库/应用语言学期刊/Abstracts_All/Merge_all_abstracts.txt'

# 写入纯文本文件
with open(output_txt_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"已成功汇总 {len(all_abstracts)} 个摘要，保存至：{output_txt_path}")
