# 读取数据
l2 <- read.csv("/Users/fafaya/Research-on-AI-generated-text-series/!!!统计分析代码及结果/L2_Comparison_Results_with_Quartiles.csv")

# 加载绘图包
library(ggplot2)
library(dplyr)

# 作图
ggplot(l2, aes(x = Metric, y = Mean_Diff, fill = Signif)) +
  geom_bar(stat = "identity", position = "dodge") +
  geom_text(aes(label = Signif), vjust = -0.5, size = 5) +
  scale_fill_manual(values = c("n.s." = "gray70", "*" = "#FFC107", "**" = "#FF7043", "***" = "#D32F2F")) +
  labs(title = "L2 Syntactic Complexity Differences (AL - CS)",
       x = "L2 Metric", y = "Mean Difference") +
  theme_minimal(base_size = 14)


# 读取数据
np <- read.csv("/Users/fafaya/Research-on-AI-generated-text-series/!!!统计分析代码及结果/Syntax_Comparison_All.csv")

# 只保留 NP Complexity 模块
np_subset <- np %>% 
  filter(Module == "NP Complexity") %>%
  select(Metric, Mean_AL, Mean_CS)

# 整理成长数据格式
np_long <- tidyr::pivot_longer(np_subset, cols = starts_with("Mean_"), names_to = "Group", values_to = "Value")
np_long$Group <- gsub("Mean_", "", np_long$Group)

# 绘图
ggplot(np_long, aes(x = Metric, y = Value, fill = Group)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "NP Complexity Features across Disciplines",
       x = "Syntactic Feature", y = "Mean Value") +
  theme_minimal(base_size = 14) +
  scale_fill_manual(values = c("AL" = "#4CAF50", "CS" = "#2196F3"))


# 添加效应量列名（确保你已提前在语法分析结果中添加 d 列，命名为 "d"）
effect <- np %>% 
  filter(Module == "NP Complexity") %>%
  select(Metric, d_value)

# 绘图
ggplot(effect, aes(x = reorder(Metric, d_value), y = d_value)) +
  geom_bar(stat = "identity", fill = "#673AB7") +
  geom_hline(yintercept = c(0.2, 0.5, 0.8), linetype = "dashed", color = "gray50") +
  coord_flip() +
  labs(title = "Effect Sizes of NP Complexity Differences (Cohen's d)",
       x = "Syntactic Feature", y = "Cohen's d") +
  theme_minimal(base_size = 14)

