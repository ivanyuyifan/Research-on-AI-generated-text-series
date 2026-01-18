import pandas as pd
import os

# --- 用户配置区 ---
# 请将下面的路径修改为您存放CSV文件的实际文件夹路径
HUMAN_FOLDER_PATH = "/Users/fafaya/Desktop/语料处理+代码/处理数据（只选取需要的指标）/Human"
AI_FOLDER_PATH = "/Users/fafaya/Desktop/语料处理+代码/处理数据（只选取需要的指标）/AI"
# --- 配置结束 ---


def final_concat_files(folder_path, prefix, id_column_name_in_co):
    """
    通过横向拼接（concat）的方式合并四个CSV文件，依赖于文件行的顺序完全一致。
    """
    print(f"--- 开始按顺序拼接: {prefix.upper()} 语料库 ---")
    
    try:
        # 构建文件路径
        path_clause = os.path.join(folder_path, f"{prefix}clause.csv")
        path_co = os.path.join(folder_path, f"{prefix}co.csv")
        path_l2 = os.path.join(folder_path, f"{prefix}L2_sca.csv")
        path_phrase = os.path.join(folder_path, f"{prefix}phrase.csv")

        # 加载所有文件
        df_clause = pd.read_csv(path_clause)
        df_co = pd.read_csv(path_co)
        df_l2 = pd.read_csv(path_l2)
        df_phrase = pd.read_csv(path_phrase)
        print("所有CSV文件加载成功。")

        # 1. 清洗并保留有意义的ID（来自co文件）
        # 使用之前最强的清洗方法
        meaningful_ids = df_co[id_column_name_in_co].astype(str).apply(os.path.basename).str.lower().str.replace('.txt', '', regex=False).str.strip()
        
        # 2. 丢弃所有原始的、无用的ID列
        df_clause = df_clause.drop(columns=['filename'])
        df_co = df_co.drop(columns=[id_column_name_in_co])
        df_l2 = df_l2.drop(columns=['filename'])
        df_phrase = df_phrase.drop(columns=['filename'])
        print("已删除所有原始ID列。")
        
        # 3. 横向拼接所有数据框 (axis=1 代表按列拼接)
        # 这会把所有表格并排放在一起
        final_df = pd.concat([df_l2, df_phrase, df_clause, df_co], axis=1)
        
        # 4. 将我们保留的有意义的ID作为第一列加回到总表中
        final_df.insert(0, 'filename', meaningful_ids)
        print("已按顺序横向拼接所有表格。")
        
        # 最终检查
        if len(final_df) > 0:
            print(f"✅ 拼接成功！最终数据集包含 {len(final_df)} 行 和 {len(final_df.columns)} 列。")
            output_filename = f"{prefix.capitalize()}_data_merged.csv"
            # 保存到脚本所在的目录
            final_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
            print(f"合并后的文件已保存为: {output_filename}")
        else:
            print("❌ 拼接失败。数据集为空。")
        
        print("-" * 40 + "\n")
        
    except Exception as e:
        print(f"在处理过程中发生错误: {e}")


if __name__ == '__main__':
    # Co-Metrix文件中有意义的ID列名
    co_metrix_id_column = 'TextID'

    # 处理Human语料
    final_concat_files(HUMAN_FOLDER_PATH, 'human', co_metrix_id_column)
    
    # 处理AI语料
    final_concat_files(AI_FOLDER_PATH, 'AI', co_metrix_id_column)