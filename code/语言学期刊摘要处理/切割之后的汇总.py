import pandas as pd

# 读取你的 L2_sca.csv 文件
df = pd.read_csv('/Users/fafaya/Desktop/L2_sca.csv')

# 确保 nwords 是整数（可能默认读成字符串）
df['nwords'] = df['nwords'].astype(int)

# 你要处理的列（排除 filename 和 nwords）
cols_to_avg = df.columns[2:]

# 计算总词数
total_words = df['nwords'].sum()

# 用于存结果
weighted_results = {}

for col in cols_to_avg:
    weighted_sum = (df[col] * df['nwords']).sum()
    weighted_avg = weighted_sum / total_words
    weighted_results[col] = round(weighted_avg, 4)  # 保留4位小数，可调整

# 加上总词数和 chunk 数
weighted_results['nwords_total'] = total_words
weighted_results['n_chunks'] = len(df)

# 结果变成一行的 dataframe
final_df = pd.DataFrame([weighted_results])

# 保存（或打印）
final_df.to_csv('/Users/fafaya/Desktop/L2_sca_merged.csv', index=False)
print(final_df)
