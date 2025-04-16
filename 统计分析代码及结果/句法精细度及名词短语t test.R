# --------------------- 文件路径 ---------------------
al_soph_path <- "/Users/fafaya/Research-on-AI-generated-text-series/数据分析结果/语言学数据分析结果/AL句法精细度结果.csv"
cs_soph_path <- "/Users/fafaya/Research-on-AI-generated-text-series/数据分析结果/计算机科学数据分析结果/CS句法精细度结果.csv"

al_np_path <- "/Users/fafaya/Research-on-AI-generated-text-series/数据分析结果/语言学数据分析结果/AL名词短语复杂度结果.csv"
cs_np_path <- "/Users/fafaya/Research-on-AI-generated-text-series/数据分析结果/计算机科学数据分析结果/CS名词短语复杂度结果.csv"

# --------------------- 读取数据 ---------------------
al_soph <- read.csv(al_soph_path)
cs_soph <- read.csv(cs_soph_path)

al_np <- read.csv(al_np_path)
cs_np <- read.csv(cs_np_path)

# --------------------- 指标设置 ---------------------
soph_metrics <- c(
  "acad_av_construction_freq",
  "acad_av_lemma_construction_freq",
  "acad_av_faith_verb_cue",
  "acad_av_delta_p_verb_cue",
  "acad_collexeme_ratio",
  "acad_construction_ttr",
  "acad_construction_attested",
  "all_av_construction_freq_log",
  "all_av_construction_freq_stdev"
)

np_metrics <- c(
  "det_all_nominal_deps_struct",
  "amod_all_nominal_deps_struct",
  "prep_all_nominal_deps_struct",
  "vmod_all_nominal_deps_struct",
  "nn_all_nominal_deps_struct",
  "rcmod_all_nominal_deps_struct"
)

# --------------------- 初始化结果表函数 ---------------------
analyze_metrics <- function(al_data, cs_data, metrics, module_name) {
  results <- data.frame(
    Metric = character(),
    Mean_AL = numeric(),
    Q1_AL = numeric(),
    Q3_AL = numeric(),
    Mean_CS = numeric(),
    Q1_CS = numeric(),
    Q3_CS = numeric(),
    Mean_Diff = numeric(),
    t_value = numeric(),
    p_value = numeric(),
    Signif = character(),
    Module = character(),
    stringsAsFactors = FALSE
  )
  
  for (metric in metrics) {
    t_result <- t.test(al_data[[metric]], cs_data[[metric]])
    
    results <- rbind(results, data.frame(
      Metric = metric,
      Mean_AL = round(mean(al_data[[metric]], na.rm = TRUE), 4),
      Q1_AL = round(quantile(al_data[[metric]], 0.25, na.rm = TRUE), 4),
      Q3_AL = round(quantile(al_data[[metric]], 0.75, na.rm = TRUE), 4),
      Mean_CS = round(mean(cs_data[[metric]], na.rm = TRUE), 4),
      Q1_CS = round(quantile(cs_data[[metric]], 0.25, na.rm = TRUE), 4),
      Q3_CS = round(quantile(cs_data[[metric]], 0.75, na.rm = TRUE), 4),
      Mean_Diff = round(mean(al_data[[metric]], na.rm = TRUE) - mean(cs_data[[metric]], na.rm = TRUE), 4),
      t_value = round(t_result$statistic, 3),
      p_value = round(t_result$p.value, 5),
      Signif = ifelse(t_result$p.value < 0.001, "***",
                      ifelse(t_result$p.value < 0.01, "**",
                             ifelse(t_result$p.value < 0.05, "*", "n.s."))),
      Module = module_name
    ))
  }
  
  return(results)
}

# --------------------- 分析两个模块 ---------------------
soph_results <- analyze_metrics(al_soph, cs_soph, soph_metrics, "Syntactic Sophistication")
np_results <- analyze_metrics(al_np, cs_np, np_metrics, "NP Complexity")

# --------------------- 合并 & 输出 ---------------------
final_results <- rbind(soph_results, np_results)

# 输出查看
print(final_results)

# 可选保存
write.csv(final_results, "/Users/fafaya/Desktop/Syntax_Comparison_All.csv", row.names = FALSE)
