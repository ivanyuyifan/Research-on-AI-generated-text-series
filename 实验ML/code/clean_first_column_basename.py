# clean_first_column_basename.py
import os
import re
import sys
import pandas as pd

def get_basename(val):
    """将路径裁剪为文件名；兼容 / 和 \\；保留NaN/空值。"""
    if pd.isna(val):
        return val
    s = str(val).strip().strip('"').strip("'")
    # 以 / 或 \ 作为分隔符切分
    parts = re.split(r'[\\/]+', s)
    return parts[-1] if parts else s

def clean_csv(in_path, out_path=None, encoding="utf-8-sig"):
    # 读取CSV（自动处理UTF-8 BOM）
    df = pd.read_csv(in_path, encoding=encoding)

    if df.shape[1] == 0:
        raise ValueError("CSV没有任何列。")

    first_col = df.columns[0]  # 第一列（可能叫TextID或filename）
    df[first_col] = df[first_col].map(get_basename)

    # 输出文件名
    if out_path is None:
        base, ext = os.path.splitext(in_path)
        out_path = f"{base}.cleaned{ext or '.csv'}"

    df.to_csv(out_path, index=False, encoding=encoding)
    return out_path

if __name__ == "__main__":
    # 用法1：命令行传入路径：python clean_first_column_basename.py your.csv [out.csv]
    # 用法2：直接在VSCode里改下面的默认输入路径，然后运行
    if len(sys.argv) >= 2:
        in_csv = sys.argv[1]
        out_csv = sys.argv[2] if len(sys.argv) >= 3 else None
    else:
        # ===== 在VSCode里直接运行时，把这行改成你的文件路径 =====
        in_csv = r"/Users/fafaya/Desktop/原始数据（包含所有指标）_副本/AIL2_sca.csv"
        out_csv = None

    out = clean_csv(in_csv, out_csv)
    print(f"已处理完成，输出文件：{out}")
