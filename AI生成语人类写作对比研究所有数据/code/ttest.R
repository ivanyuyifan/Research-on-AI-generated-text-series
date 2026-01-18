# --- 用户配置区 ---
# 请将文件路径修改为您电脑上的绝对路径
file_path <- "/Users/fafaya/Desktop/语料处理+代码/合并后的语料/Final_Master_Dataset.csv"
output_path <- "/Users/fafaya/Desktop/语料处理+代码/数据分析结果/T-Test_Results_with_Median_R.csv"
# --- 配置结束 ---


# --- 準備工作 ---
# 1. 安装并加载必要的包
# 如果您是第一次使用这些包，请取消下面两行的注释并运行一次来安装它们
# install.packages("tidyverse")
# install.packages("effsize")

library(tidyverse) # 用于数据处理和读取
library(effsize)   # 用于计算Cohen's d效应量


# --- 主分析函数 ---
run_full_analysis_in_R <- function(filepath, output_filepath) {
  
  print("--- 开始使用R进行t检验 (包含Median, Q1, Q3) ---")
  
  # 1. 读取数据
  tryCatch({
    master_df <- read_csv(filepath, show_col_types = FALSE)
    print(paste("成功读取文件:", filepath))
  }, error = function(e) {
    stop(paste("错误：无法找到或读取文件。请检查路径是否正确:", filepath))
  })
  
  # 2. 识别指标列
  metric_columns <- setdiff(names(master_df), c("filename", "Author_Type"))
  print(paste("将对", length(metric_columns), "个语言学指标进行检验..."))
  
  # 3. 创建空列表存储结果
  results_list <- list()
  
  # 4. 循环分析每个指标
  for (metric in metric_columns) {
    
    formula <- as.formula(paste(metric, "~ Author_Type"))
    
    # 错误处理
    t_test_result <- tryCatch({ t.test(formula, data = master_df) }, error = function(e) { list(statistic = NA, p.value = NA) })
    cohen_d_result <- tryCatch({ cohen.d(formula, data = master_df) }, error = function(e) { list(estimate = NA) })
    
    # --- 新增：计算更全面的描述性统计 ---
    stats_summary <- master_df %>%
      group_by(Author_Type) %>%
      summarise(
        Mean = mean(.data[[metric]], na.rm = TRUE),
        SD = sd(.data[[metric]], na.rm = TRUE),
        Median = median(.data[[metric]], na.rm = TRUE),
        Q1 = quantile(.data[[metric]], 0.25, na.rm = TRUE),
        Q3 = quantile(.data[[metric]], 0.75, na.rm = TRUE),
        .groups = 'drop'
      )
    
    human_stats <- stats_summary %>% filter(Author_Type == "Human")
    ai_stats <- stats_summary %>% filter(Author_Type == "AI")
    
    # 将结果存入临时data.frame
    temp_result <- data.frame(
      Metric = metric,
      T_Statistic = t_test_result$statistic,
      p_value = t_test_result$p.value,
      Cohens_d = cohen_d_result$estimate,
      Mean_Human = human_stats$Mean,
      SD_Human = human_stats$SD,
      Median_Human = human_stats$Median,
      Q1_Human = human_stats$Q1,
      Q3_Human = human_stats$Q3,
      Mean_AI = ai_stats$Mean,
      SD_AI = ai_stats$SD,
      Median_AI = ai_stats$Median,
      Q1_AI = ai_stats$Q1,
      Q3_AI = ai_stats$Q3
    )
    
    results_list[[metric]] <- temp_result
  }
  
  # 5. 合并所有结果
  results_df <- do.call(rbind, results_list)
  
  # 6. Bonferroni 校正
  num_tests <- length(metric_columns)
  results_df$p_adjusted_bonferroni <- pmin(results_df$p_value * num_tests, 1.0)
  
  # 7. 整理最终表格
  results_df <- results_df %>%
    mutate(`Significant (p_adj < .05)` = ifelse(p_adjusted_bonferroni < 0.05, "Yes", "No")) %>%
    arrange(p_adjusted_bonferroni) %>%
    # 调整列顺序以获得更好的可读性
    select(
      Metric, `Significant (p_adj < .05)`, p_adjusted_bonferroni, p_value, Cohens_d, T_Statistic,
      Mean_Human, SD_Human, Median_Human, Q1_Human, Q3_Human,
      Mean_AI, SD_AI, Median_AI, Q1_AI, Q3_AI
    )
  
  # 8. 保存并（尝试）打印结果
  output_dir <- dirname(output_filepath)
  if (!dir.exists(output_dir)) { dir.create(output_dir, recursive = TRUE) }
  
  write_csv(results_df, output_filepath)
  print(paste("✅ 操作成功！包含Median和Quartiles的详细结果已保存至:", output_filepath))
  print("--------------------------------------------------")
  
  print("--- 尝试在屏幕上打印结果 (此步若报错可忽略) ---")
  print(as.data.frame(results_df), n = nrow(results_df))
}

# --- 运行主函数 ---
run_full_analysis_in_R(file_path, output_path)