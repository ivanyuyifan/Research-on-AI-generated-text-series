# visualization_rf.py
# 运行前请确认 outputs 文件夹中已有随机森林输出结果

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['axes.unicode_minus'] = False  # 避免负号显示成方块

# ----------------------
# 1) 读入结果文件（你的路径保持不变）
# ----------------------
metrics_path = "/Users/fafaya/Desktop/语料处理+代码/实验ML/outputs/第二次跑的结果（去掉DES增加ArticleID）/rf_cv_metrics_summary.csv"
imp_path     = "/Users/fafaya/Desktop/语料处理+代码/实验ML/outputs/第二次跑的结果（去掉DES增加ArticleID）/rf_feature_importance.csv"
master_xlsx  = "/Users/fafaya/Desktop/语料处理+代码/实验ML/outputs/master_features.xlsx"  # 这是 .xlsx

metrics = pd.read_csv(metrics_path)
imp_raw = pd.read_csv(imp_path)

print("=== 模型性能汇总 ===")
print(metrics)

# ----------------------
# 2) Figure 6：特征重要性（使用健壮函数）
# ----------------------
from matplotlib.ticker import FuncFormatter

def plot_feature_importance(csv_path: str, top_n: int = 15, save_path: str | None = None):
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]

    cand_importance = ["mean_importance", "importance", "importances_mean", "imp", "score"]
    imp_col = next((c for c in cand_importance if c in df.columns), None)
    if imp_col is None:
        raise ValueError(f"找不到重要性列，候选名：{cand_importance}；实际列名：{list(df.columns)}")

    cand_feature = ["feature", "feature_name", "name", "variable", "feat"]
    feat_col = next((c for c in cand_feature if c in df.columns), None)
    if feat_col is None:
        first_col = df.columns[0]
        if first_col != imp_col and df[first_col].dtype == "object":
            feat_col = first_col
        else:
            df = df.reset_index().rename(columns={"index": "feature"})
            feat_col = "feature"

    df_top = df[[feat_col, imp_col]].copy().sort_values(imp_col, ascending=False).head(top_n)

    plt.figure(figsize=(8, 6))
    sns.barplot(data=df_top, x=imp_col, y=feat_col)  # 不设 palette，避免 FutureWarning
    plt.title("Figure 6. Top 15 Linguistic Features by Importance", fontsize=13, pad=10)
    plt.xlabel("Mean Importance", fontsize=11)
    plt.ylabel("Feature", fontsize=11)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.3f}"))
    for p in plt.gca().patches:
        w = p.get_width()
        y = p.get_y() + p.get_height()/2
        plt.gca().text(w + (df_top[imp_col].max()*0.01), y, f"{w:.3f}", va="center", fontsize=9)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=600, bbox_inches="tight")
        print(f"[Saved] {save_path}")
    plt.show()

plot_feature_importance(
    csv_path=imp_path,
    top_n=15,
    save_path="/Users/fafaya/Desktop/语料处理+代码/实验ML/outputs/Figure6_FeatureImportance.png"
)

# ----------------------
# 3) Figure 7：特征相关性热图（只画 Top-15，且仅数值列；用 read_excel）
# ----------------------
# 读取 Excel（必须用 read_excel；若缺 openpyxl 可先 pip install openpyxl）
try:
    df_master = pd.read_excel(master_xlsx)  # engine="openpyxl" 如需显式指定可加
except Exception as e:
    raise RuntimeError(f"读取 {master_xlsx} 失败，请确认路径与文件类型：{e}")

# 自动识别列名（与上面相同逻辑）
cols_lower = [c.strip().lower() for c in imp_raw.columns]
imp_raw.columns = cols_lower
feat_col = "feature" if "feature" in cols_lower else ("feature_name" if "feature_name" in cols_lower else imp_raw.columns[0])
imp_col  = "mean_importance" if "mean_importance" in cols_lower else ("importance" if "importance" in cols_lower else imp_raw.columns[1])

top_feats = (imp_raw[[feat_col, imp_col]]
             .sort_values(imp_col, ascending=False)
             .head(15)[feat_col]
             .tolist())

# 只保留 master 中存在且为数值的列
num_df = df_master.select_dtypes(include="number")
feats_available = [f for f in top_feats if f in num_df.columns]

if len(feats_available) >= 2:
    corr = num_df[feats_available].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, cmap="RdBu_r", center=0, annot=False, square=False)
    plt.title("Figure 7. Correlation among Top Linguistic Features", fontsize=13, pad=10)
    plt.tight_layout()
    plt.savefig("/Users/fafaya/Desktop/语料处理+代码/实验ML/outputs/Figure7_FeatureCorrelation.png",
                dpi=600, bbox_inches="tight")
    print("[Saved] /Users/fafaya/Desktop/语料处理+代码/实验ML/outputs/Figure7_FeatureCorrelation.png")
    plt.show()
else:
    print("⚠️ Top 特征在 master_features 中匹配太少，跳过相关性热图。检查列名是否一致。")
