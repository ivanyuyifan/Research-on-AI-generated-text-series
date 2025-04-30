import os
import shutil

# 原始根目录（包含多个子文件夹，每个是一个期刊）
source_root = '/Users/fafaya/Research-on-AI-generated-text-series/语料库/计算机科学期刊'

# 目标输出目录（统一合并的文件夹）
target_dir = '/Users/fafaya/Desktop/CS_Abstracts_All'

# 创建目标目录（若不存在）
os.makedirs(target_dir, exist_ok=True)

# 遍历每个子文件夹（期刊）
for journal_folder in os.listdir(source_root):
    journal_path = os.path.join(source_root, journal_folder)
    if os.path.isdir(journal_path):
        for filename in os.listdir(journal_path):
            if filename.endswith('.txt'):
                src_file = os.path.join(journal_path, filename)
                # 为防止重名文件，用子文件夹名+原文件名组合成新文件名
                safe_filename = f"{journal_folder}_{filename}"
                dst_file = os.path.join(target_dir, safe_filename)
                shutil.copy(src_file, dst_file)

print(f"✅ 所有摘要文件已复制并集中保存至：{target_dir}")
