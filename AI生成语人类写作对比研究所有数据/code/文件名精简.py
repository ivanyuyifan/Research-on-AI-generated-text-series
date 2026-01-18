import pandas as pd
import os

# --- 用户配置区 (绝对路径) ---
# 您要修改的源文件的绝对路径
MASTER_FILE_PATH = '/Users/fafaya/Desktop/语料处理+代码/合并后的语料/Final_Master_Dataset.csv'
# --- 配置结束 ---

def final_clean_filename(filepath):
    """
    读取CSV文件，确保'filename'列只包含最后的文件名部分。
    """
    print(f"--- 开始最终清理 '{os.path.basename(filepath)}' 的 'filename' 列 ---")
    
    try:
        # 1. 读取您的主数据集
        df = pd.read_csv(filepath)
        print(f"成功读取文件:\n'{filepath}'")

        # 打印清理前的几个文件名作为示例
        print("\n清理前的'filename'列（前5行）:")
        print(df['filename'].head().to_string(index=False))

        # 2. 使用 os.path.basename 清理'filename'列
        # 这个函数是专门用来从一个路径中提取最后的文件名部分的，非常可靠。
        df['filename'] = df['filename'].apply(os.path.basename)
        
        print("\n'filename'列已清理完毕。")

        # 打印清理后的文件名作为对比
        print("\n清理后的'filename'列（前5行）:")
        print(df['filename'].head().to_string(index=False))

        # 3. 将修改后的数据覆盖保存回原文件
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"\n✅ 操作成功！已将最干净的数据保存回:\n'{filepath}'")

    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 '{filepath}'。请确保路径完全正确。")
    except KeyError:
        print(f"❌ 错误：在文件中找不到名为 'filename' 的列。")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")


if __name__ == '__main__':
    final_clean_filename(MASTER_FILE_PATH)