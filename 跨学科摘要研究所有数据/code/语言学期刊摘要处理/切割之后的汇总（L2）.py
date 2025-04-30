import pandas as pd

# 设置路径
input_csv = '/Users/fafaya/Desktop/语言学期刊L2结果（单篇版）_sca.csv'

# 读取CSV
df = pd.read_csv(input_csv)

# 去掉 filename 列，仅保留数值列
metrics = df.columns.tolist()
metrics.remove('filename')

# 计算总词数
total_words = df['nwords'].sum()

# 构建一个新字典用于存储加权平均
weighted_avg = {'nwords_total': total_words, 'n_chunks': len(df)}

# 对每个其他指标做加权平均
for metric in metrics:
    if metric != 'nwords':
        weighted_sum = (df[metric] * df['nwords']).sum()
        weighted_avg[metric] = round(weighted_sum / total_words, 4)

# 转成DataFrame输出
result_df = pd.DataFrame([weighted_avg])
print(result_df)

# 可选：保存输出
result_df.to_csv('/Users/fafaya/Desktop/L2_sca_weighted_summary.csv', index=False)
print("✅ 汇总结果已保存至桌面：L2_sca_weighted_summary.csv")
