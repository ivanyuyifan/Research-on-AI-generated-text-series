library(effsize)

# 设置路径
al_l2_path <- "/Users/fafaya/Research-on-AI-generated-text-series/数据分析结果/语言学数据分析结果/语言学期刊L2结果（单篇版）_sca.csv"
cs_l2_path <- "/Users/fafaya/Research-on-AI-generated-text-series/数据分析结果/计算机科学数据分析结果/CS L2结果（分割版）_sca.csv"

# 读取数据
al_l2 <- read.csv(al_l2_path)
cs_l2 <- read.csv(cs_l2_path)

# 指标列表（14个L2指标）
l2_metrics <- c("MLS", "MLT", "MLC", "C_S", "VP_T", "C_T",
                "DC_C", "DC_T", "T_S", "CT_T", "CP_T",
                "CP_C", "CN_T", "CN_C")

# 初始化结果表
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
  d_value = numeric(),
  d_magnitude = character(),
  Signif = character(),
  stringsAsFactors = FALSE
)

# 循环 t 检验 + 四分位数计算
for (metric in l2_metrics) {
  t_result <- t.test(al_l2[[metric]], cs_l2[[metric]])
  d_result <- cohen.d(al_l2[[metric]], cs_l2[[metric]])
  d_val <- round(d_result$estimate, 3)
  d_mag <- as.character(d_result$magnitude)
  
  results <- rbind(results, data.frame(
    Metric = metric,
    Mean_AL = round(mean(al_l2[[metric]], na.rm = TRUE), 3),
    Q1_AL = round(quantile(al_l2[[metric]], 0.25, na.rm = TRUE), 3),
    Q3_AL = round(quantile(al_l2[[metric]], 0.75, na.rm = TRUE), 3),
    Mean_CS = round(mean(cs_l2[[metric]], na.rm = TRUE), 3),
    Q1_CS = round(quantile(cs_l2[[metric]], 0.25, na.rm = TRUE), 3),
    Q3_CS = round(quantile(cs_l2[[metric]], 0.75, na.rm = TRUE), 3),
    Mean_Diff = round(mean(al_l2[[metric]], na.rm = TRUE) - mean(cs_l2[[metric]], na.rm = TRUE), 3),
    t_value = round(t_result$statistic, 3),
    p_value = round(t_result$p.value, 5),
    d_value = d_val,
    d_magnitude = d_mag,
    Signif = ifelse(t_result$p.value < 0.001, "***",
                    ifelse(t_result$p.value < 0.01, "**",
                           ifelse(t_result$p.value < 0.05, "*", "n.s.")))
  ))
}

# 循环结束后，进行 Bonferroni 校正
results$adjusted_p <- round(p.adjust(results$p_value, method = "bonferroni"), 5)

# 添加显著性标注（使用调整后的 p 值）
results$Bonferroni_Signif <- ifelse(results$adjusted_p < 0.001, "***",
                              ifelse(results$adjusted_p < 0.01, "**",
                              ifelse(results$adjusted_p < 0.05, "*", "n.s.")))

# 输出结果
print(results)

# 可选：保存到桌面
write.csv(results, "/Users/fafaya/Desktop/L2_Comparison_Results_with_Quartiles.csv", row.names = FALSE)
