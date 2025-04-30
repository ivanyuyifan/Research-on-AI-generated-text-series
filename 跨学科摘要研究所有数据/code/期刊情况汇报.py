import os
import numpy as np

def count_words(text):
    # 简单分词计数
    return len(text.split())

def analyze_corpus(folder_path):
    word_counts = []
    filenames = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                count = count_words(text)
                word_counts.append(count)
                filenames.append(filename)

    num_files = len(word_counts)
    total_words = sum(word_counts)
    min_words = np.min(word_counts)
    max_words = np.max(word_counts)
    mean_words = np.mean(word_counts)
    std_words = np.std(word_counts)

    print(f"📁 语料路径：{folder_path}")
    print(f"📄 摘要总数：{num_files}")
    print(f"🔢 总词数：{total_words}")
    print(f"📉 最短摘要：{min_words} 词")
    print(f"📈 最长摘要：{max_words} 词")
    print(f"📊 平均长度：{mean_words:.2f} 词")
    print(f"📐 标准差：{std_words:.2f} 词")
    print("-" * 50)

# =================== 执行 ===================

# 语言学
al_path = "/Users/fafaya/Research-on-AI-generated-text-series/Abstracts_All_AL/AL_Abstracts_All"
analyze_corpus(al_path)

# 计算机
cs_path = "/Users/fafaya/Research-on-AI-generated-text-series/Abstracts_All_CS/CS_Abstracts_All"
analyze_corpus(cs_path)
