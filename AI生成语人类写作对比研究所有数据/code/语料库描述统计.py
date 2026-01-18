# -*- coding: utf-8 -*-
"""
Corpus descriptives for AI vs Human abstracts

功能：
1) 读取两个目录下的 .txt 文件，统计每个文件的词数（英文词）
2) 计算各组的描述性统计（Number, Words, Maximum, Minimum, Mean, SD）
3) 输出 per-file 与 summary 两类结果到指定目录
4) 生成 Markdown 与 LaTeX 表格（可直接粘贴到论文）

作者：你
"""

import os
import re
import csv
from pathlib import Path
import statistics as stats

# ========= 路径配置（按需修改） =========
AI_DIR = Path("/Users/fafaya/Desktop/语料处理+代码/废弃语料/TAASSC_Input_AI")
HUMAN_DIR = Path("/Users/fafaya/Desktop/语料处理+代码/废弃语料/TAASSC_Input_Human")
OUT_DIR = Path("/Users/fafaya/Desktop/语料处理+代码/数据分析结果")

# 显示用的标签（表格里怎么写）
DISPLAY_NAME = {
    "AI": "AI abstracts",
    "Human": "Human abstracts",
}

# ========== 词计数：英文词口径 ==========
# 说明：只统计字母序列，允许内部撇号（e.g., don't, researchers’）
WORD_PATTERN = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")

def count_words_en(text: str) -> int:
    return len(WORD_PATTERN.findall(text))

def safe_read_text(path: Path) -> str:
    # 尝试常见编码，避免报错
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return path.read_text(encoding=enc, errors="ignore")
        except Exception:
            continue
    return ""

def collect_counts(folder: Path, group_label: str):
    """
    返回：[(group, filepath, filename, word_count), ...]
    """
    rows = []
    if not folder.exists():
        print(f"[WARN] 路径不存在：{folder}")
        return rows
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            if not f.lower().endswith(".txt"):
                continue
            p = Path(root) / f
            txt = safe_read_text(p)
            wc = count_words_en(txt)
            rows.append((group_label, str(p), f, wc))
    return rows

def summarize(counts_list):
    """
    输入：某一组的词数列表 [w1, w2, ...]
    返回：字典
    """
    if not counts_list:
        return {
            "Number": 0, "Words": 0, "Maximum": 0, "Minimum": 0,
            "Mean": 0.0, "SD": 0.0
        }
    n = len(counts_list)
    total = sum(counts_list)
    mx = max(counts_list)
    mn = min(counts_list)
    mean = total / n
    # 学术写作常用样本标准差
    sd = stats.stdev(counts_list) if n > 1 else 0.0
    return {
        "Number": n,
        "Words": total,
        "Maximum": mx,
        "Minimum": mn,
        "Mean": mean,
        "SD": sd
    }

def ensure_outdir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def save_per_file_csv(rows, out_path: Path):
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Group", "FilePath", "FileName", "WordCount"])
        for r in rows:
            w.writerow(r)

def save_summary_csv(summary_rows, out_path: Path):
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Group", "Number", "Words", "Maximum", "Minimum", "Mean", "SD"])
        for s in summary_rows:
            w.writerow([
                s["Group"], s["Number"], s["Words"], s["Maximum"], s["Minimum"],
                f"{s['Mean']:.2f}", f"{s['SD']:.2f}"
            ])

def save_markdown_table(summary_rows, out_path: Path, title="Table 1. Descriptive statistics of the corpus."):
    # 期刊风 Markdown 风格
    lines = []
    lines.append(title)
    lines.append("")
    header = "| Group | Number | Words | Maximum | Minimum | Mean | SD |"
    sep    = "|:----- | ------:| -----:| -------:| -------:| ----:| --:|"
    lines.append(header)
    lines.append(sep)
    for s in summary_rows:
        lines.append(
            f"| {s['Group']} | {s['Number']:,} | {s['Words']:,} | {s['Maximum']:,} | {s['Minimum']:,} | {s['Mean']:.2f} | {s['SD']:.2f} |"
        )
    out_path.write_text("\n".join(lines), encoding="utf-8")

def save_latex_table(summary_rows, out_path: Path, caption="Descriptive statistics of the corpus.", label="tab:descriptives"):
    # LaTeX 表格（booktabs 风格）
    lines = []
    lines.append(r"\begin{table}[t]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{lrrrrrr}")
    lines.append(r"\toprule")
    lines.append(r" & Number & Words & Maximum & Minimum & Mean & SD \\")
    lines.append(r"\midrule")
    for s in summary_rows:
        lines.append(
            f"{s['Group']} & {s['Number']:,} & {s['Words']:,} & {s['Maximum']:,} & {s['Minimum']:,} & {s['Mean']:.2f} & {s['SD']:.2f} \\\\"
        )
    lines.append(r"\bottomrule")
    lines.append(rf"\caption{{{caption}}}")
    lines.append(rf"\label{{{label}}}")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")
    out_path.write_text("\n".join(lines), encoding="utf-8")

def main():
    ensure_outdir(OUT_DIR)

    # 1) 收集每文件词数
    ai_rows = collect_counts(AI_DIR, "AI")
    human_rows = collect_counts(HUMAN_DIR, "Human")
    all_rows = ai_rows + human_rows

    # 2) 输出每文件词数
    per_file_csv = OUT_DIR / "per_file_counts.csv"
    save_per_file_csv(all_rows, per_file_csv)

    # 3) 汇总统计
    ai_counts = [r[3] for r in ai_rows]
    hm_counts = [r[3] for r in human_rows]

    ai_sum = summarize(ai_counts)
    hm_sum = summarize(hm_counts)

    # 显示名（论文表格里更自然）
    ai_label = DISPLAY_NAME.get("AI", "AI")
    hm_label = DISPLAY_NAME.get("Human", "Human")

    summary_rows = [
        {"Group": ai_label, **ai_sum},
        {"Group": hm_label, **hm_sum},
    ]

    # 4) 保存汇总
    summary_csv = OUT_DIR / "descriptives.csv"
    save_summary_csv(summary_rows, summary_csv)

    # 5) 生成 Markdown/LaTeX 表
    md_path = OUT_DIR / "table1_descriptives.md"
    tex_path = OUT_DIR / "table1_descriptives.tex"
    save_markdown_table(summary_rows, md_path)
    save_latex_table(summary_rows, tex_path)

    # 6) 控制台简要输出
    print("\n=== Descriptive statistics of the corpus (per-file word counts) ===\n")
    for s in summary_rows:
        print(
            f"{s['Group']:<16}  Number={s['Number']:>4},  Words={s['Words']:,},  "
            f"Max={s['Maximum']},  Min={s['Minimum']},  Mean={s['Mean']:.2f},  SD={s['SD']:.2f}"
        )
    print(f"\n[Saved] {per_file_csv}")
    print(f"[Saved] {summary_csv}")
    print(f"[Saved] {md_path}")
    print(f"[Saved] {tex_path}\n")

if __name__ == "__main__":
    main()
