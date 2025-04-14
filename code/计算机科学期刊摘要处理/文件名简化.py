import os

# 你的集中语料文件夹路径
folder_path = '/Users/fafaya/Desktop/CS_Abstracts_All'

# 获取所有 .txt 文件（按原文件名排序）
txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

# 遍历并重命名
for idx, filename in enumerate(txt_files, 1):
    new_filename = f'abs_{idx:03d}.txt'  # 例如：abs_001.txt
    src_path = os.path.join(folder_path, filename)
    dst_path = os.path.join(folder_path, new_filename)
    os.rename(src_path, dst_path)

print(f"✅ 已成功重命名 {len(txt_files)} 个摘要文件为简洁格式 abs_###.txt")
