# rf_experiment.py
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List
from sklearn.model_selection import StratifiedKFold, GroupKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold, SelectKBest, mutual_info_classif
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.inspection import permutation_importance

# ====== 路径配置 ======
BASE = Path("/Users/fafaya/Desktop/语料处理+代码/实验ML")
MASTER_CSV = Path("/Users/fafaya/Desktop/语料处理+代码/实验ML/outputs/master_features.xlsx")
OUT = BASE / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
N_SPLITS = 5
K_SELECT = 40         # 互信息选择多少个特征，可改为 20/30/50 做敏感性分析
CORR_TH = 0.95        # 删除高度相关的冗余特征

# ====== 读数与预处理 ======
def load_data(path: Path):
    df = pd.read_excel(path)
    assert "filename" in df.columns and "Label" in df.columns
    # 标签编码
    y = df["Label"].map({"Human":1, "AI":0}).values
    # groups（这样模型就不会在不同折里“偷看”同一篇论文的内容。）
    groups = df["ArticleID"].values if "ArticleID" in df.columns else None

    # 数值特征：除了"filename", "Label"之外
    drop_cols = [c for c in ["filename", "Label"] if c in df.columns]
    X = df.drop(columns=drop_cols)

    # ✅ 删除篇幅相关列
    X = X.drop(columns=[c for c in X.columns if c.startswith("DES")], errors="ignore")

    # 只保留数值列
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    X = X[num_cols].copy()

    # 去掉全常数列/全空列
    nunique = X.nunique()
    keep = nunique[nunique > 1].index
    X = X[keep]

    return X, y, groups, num_cols

def drop_high_corr(X: pd.DataFrame, th: float=0.95) -> pd.DataFrame:
    if X.shape[1] < 2:
        return X
    corr = X.corr(numeric_only=True).abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    drop_cols = [col for col in upper.columns if any(upper[col] > th)]
    return X.drop(columns=drop_cols, errors="ignore")

# ====== 单折训练与评估 ======
def run_fold(X_tr, y_tr, X_te, y_te, feature_names) -> Tuple[dict, pd.Series]:
    # 1) 缺失值填充（中位数）
    imp = SimpleImputer(strategy="median")
    X_tr = imp.fit_transform(X_tr)
    X_te = imp.transform(X_te)

    # 2) 方差过滤（极低方差）
    vt = VarianceThreshold(1e-12)
    X_tr = vt.fit_transform(X_tr)
    X_te = vt.transform(X_te)
    feat_after_vt = feature_names[vt.get_support()]

    # 3) 互信息筛特征
    k = min(K_SELECT, X_tr.shape[1])
    skb = SelectKBest(mutual_info_classif, k=k)
    X_tr = skb.fit_transform(X_tr, y_tr)
    X_te = skb.transform(X_te)
    feat_selected = feat_after_vt[skb.get_support()]

    # 4) 随机森林
    rf = RandomForestClassifier(
        n_estimators=800,
        max_depth=None,
        max_features="sqrt",
        min_samples_leaf=1,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight=None  # 类别均衡的话可不设
    )
    rf.fit(X_tr, y_tr)

    # 5) 评估
    prob = rf.predict_proba(X_te)[:,1]
    pred = (prob >= 0.5).astype(int)

    metrics = {
        "accuracy": accuracy_score(y_te, pred),
        "precision": precision_score(y_te, pred, zero_division=0),
        "recall": recall_score(y_te, pred, zero_division=0),
        "f1": f1_score(y_te, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_te, prob)
    }

    # 6) 排列重要度（在验证集上，避免训练集偏见）
    pi = permutation_importance(rf, X_te, y_te, n_repeats=10, random_state=RANDOM_STATE, n_jobs=-1)
    imp_series = pd.Series(pi.importances_mean, index=feat_selected)

    return metrics, imp_series

def main():
    X, y, groups, all_names = load_data(MASTER_CSV)

    # 预先做一次高相关过滤（仅在训练集内部做更严谨，这里先做一次全局弱过滤以提速）
    X = drop_high_corr(X, th=CORR_TH)
    feature_names = np.array(X.columns)

    # 交叉验证器
    if groups is not None:
        splitter = GroupKFold(n_splits=N_SPLITS)
        split_iter = splitter.split(X, y, groups=groups)
    else:
        splitter = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
        split_iter = splitter.split(X, y)

    fold_metrics = []
    imp_list = []

    for fold, (tr, te) in enumerate(split_iter, start=1):
        X_tr, X_te = X.iloc[tr], X.iloc[te]
        y_tr, y_te = y[tr], y[te]

        m, imp = run_fold(X_tr, y_tr, X_te, y_te, feature_names)
        m["fold"] = fold
        fold_metrics.append(m)
        imp_list.append(imp)

        print(f"[Fold {fold}] acc={m['accuracy']:.3f} f1={m['f1']:.3f} auc={m['roc_auc']:.3f}")

    # 汇总指标
    df_metrics = pd.DataFrame(fold_metrics)
    avg = df_metrics.drop(columns="fold").mean().to_dict()
    std = df_metrics.drop(columns="fold").std(ddof=0).to_dict()
    print("\n=== CV Mean ± SD ===")
    for k in ["accuracy","precision","recall","f1","roc_auc"]:
        print(f"{k}: {avg[k]:.3f} ± {std[k]:.3f}")

    # 汇总特征重要度（跨折取均值，并给出出现次数）
    imp_df = pd.concat(imp_list, axis=1).fillna(0)
    imp_df["mean_importance"] = imp_df.mean(axis=1)
    imp_df["nonzero_counts"] = (imp_df.iloc[:,:-1] != 0).sum(axis=1)
    imp_df = imp_df.sort_values("mean_importance", ascending=False)

    # 输出
    OUT.mkdir(parents=True, exist_ok=True)
    df_metrics.to_csv(OUT / "rf_cv_metrics_folds.csv", index=False)
    (pd.DataFrame({"metric":[k for k in avg.keys()], "mean":[avg[k] for k in avg.keys()], "sd":[std[k] for k in std.keys()]} )
        .to_csv(OUT / "rf_cv_metrics_summary.csv", index=False))
    imp_df.to_csv(OUT / "rf_feature_importance.csv")

    print(f"\nSaved metrics to: {OUT/'rf_cv_metrics_summary.csv'}")
    print(f"Saved feature importance to: {OUT/'rf_feature_importance.csv'}")

    # 打印 Top-15 重要特征
    print("\nTop-15 features:")
    print(imp_df[["mean_importance","nonzero_counts"]].head(15).round(6))

if __name__ == "__main__":
    main()
