import pandas as pd
import os

# --- 用户配置区 (已更新为绝对路径) ---
HUMAN_FILE = '/Users/fafaya/Desktop/语料处理+代码/合并后的语料/Human_data_merged.csv'
AI_FILE = '/Users/fafaya/Desktop/语料处理+代码/合并后的语料/Ai_data_merged.csv' # 注意：这里根据您的输入使用了'Ai'

# 定义输出文件夹路径
OUTPUT_FOLDER = '/Users/fafaya/Desktop/语料处理+代码/合并后的语料'
# 定义输出文件名
OUTPUT_FILENAME = 'Final_Master_Dataset.csv'
# 将输出文件夹和文件名合并成一个完整的绝对路径
OUTPUT_FULL_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
# --- 配置结束 ---

def combine_datasets(human_csv_path, ai_csv_path, output_csv_path):
    """
    将人类和AI的数据集合并成一个用于统计分析的主数据集。
    """
    print("--- 开始合并最终数据集 ---")
    
    try:
        # 1. 读取两个已合并的数据文件
        df_human = pd.read_csv(human_csv_path)
        df_ai = pd.read_csv(ai_csv_path)
        print(f"成功读取 '{os.path.basename(human_csv_path)}' (包含 {len(df_human)} 行)。")
        print(f"成功读取 '{os.path.basename(ai_csv_path)}' (包含 {len(df_ai)} 行)。")

        # 2. 为每个数据集添加分组变量列 'Author_Type'
        df_human['Author_Type'] = 'Human'
        df_ai['Author_Type'] = 'AI'
        print("已成功添加 'Author_Type' 列。")

        # 3. 将两个数据集上下拼接
        final_df = pd.concat([df_human, df_ai], ignore_index=True)
        print("已将两个数据集合并。")

        # 4. 验证合并结果
        num_rows, num_cols = final_df.shape
        print("\n--- 最终结果验证 ---")
        print(f"合并后的主数据集包含 {num_rows} 行 和 {num_cols} 列。")
        print("作者类型分布情况:")
        print(final_df['Author_Type'].value_counts())
        print("---------------------\n")

        # 5. 保存最终的主数据集
        final_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ 操作成功！最终的主数据文件已保存至:\n'{output_csv_path}'")
        print("现在您可以开始进行t检验等统计分析了。")

    except FileNotFoundError as e:
        print(f"❌ 错误：找不到文件。请仔细检查您在代码中设置的绝对路径是否完全正确。")
        print(f"无法找到的文件路径: {e.filename}")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")


if __name__ == '__main__':
    combine_datasets(HUMAN_FILE, AI_FILE, OUTPUT_FULL_PATH)