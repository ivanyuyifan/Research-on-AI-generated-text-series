import os
import shutil

# 设置根目录和输出目录
root_dir = '/Users/fafaya/Research-on-AI-generated-text-series/语料库/应用语言学期刊'
target_dir = '/Users/fafaya/Desktop/AL_Abstracts_All'

# 创建目标文件夹
os.makedirs(target_dir, exist_ok=True)

# 统计编号
abs_count = 1

# 遍历五个期刊文件夹
for journal_folder in os.listdir(root_dir):
    journal_path = os.path.join(root_dir, journal_folder)
    if os.path.isdir(journal_path):
        for article_folder in os.listdir(journal_path):
            article_path = os.path.join(journal_path, article_folder)
            if os.path.isdir(article_path):
                for file in os.listdir(article_path):
                    if file.endswith('.txt'):
                        src = os.path.join(article_path, file)
                        dst = os.path.join(target_dir, f'abs_{abs_count:03d}.txt')
                        shutil.copy(src, dst)
                        abs_count += 1

print(f"✅ 成功提取并重命名 {abs_count - 1} 篇摘要，保存至：{target_dir}")
