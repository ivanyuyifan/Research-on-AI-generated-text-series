# --- 1. 安装并加载必要的R包 ---
# 如果您的环境中没有安装这些包，请先取消下面的注释并运行
# install.packages("ggplot2")
# install.packages("patchwork")
# install.packages("dplyr")
# install.packages("showtext") # 新增：用于解决中文字体显示问题

library(ggplot2)
library(patchwork)
library(dplyr)
library(showtext) # 新增


# --- 1.1. 中文字体配置 (关键步骤) ---
# 更新：您遇到的“杂”字无法显示的问题，是因为当前加载的字体库不完整或存在渲染问题。
# 为了确保代码在不同电脑上都能稳定运行，我们直接从Google Fonts服务器下载并使用 "Noto Sans SC" 字体。
# "Noto Sans SC" 是一个高质量的开源字体，包含了非常全面的简体中文字符，可以解决缺字问题。
# 注意：首次运行此代码需要网络连接以下载字体。

font_add_google("Noto Sans SC", "my_font") # 下载并注册字体，别名为 "my_font"

# 自动开启showtext功能，这样后续所有ggplot图都会使用我们加载的字体
showtext_auto()


# --- 2. 准备数据 ---
# 数据严格按照您提供的截图中的表格6和表格8录入
# 只包含通过统计显著性检验 (p < .05) 的指标

# 表格6的数据: 句子复杂度
table6_data <- data.frame(
  Metric = c("MLS", "MLT", "CP/T", "CP/C", "CN/T"),
  AL = c(27.80, 26.14, 1.02, 0.66, 4.05),
  CS = c(24.71, 23.47, 0.67, 0.50, 3.48)
)

# 表格8的数据: 名词短语复杂度
table8_data <- data.frame(
  Metric = c("Det/N", "Adj/N", "Prep/N", "NN/N", "RC/N"),
  AL = c(0.28, 0.36, 0.30, 0.21, 0.02),
  CS = c(0.37, 0.46, 0.26, 0.32, 0.03)
)

# --- 3. 数据转换与整理 ---
# 将宽数据转换为长数据，以方便ggplot2进行分组绘图
table6_long <- table6_data %>%
  tidyr::pivot_longer(cols = c(AL, CS), names_to = "Discipline", values_to = "Value")

table8_long <- table8_data %>%
  tidyr::pivot_longer(cols = c(AL, CS), names_to = "Discipline", values_to = "Value")

# 为了图例显示更美观，将学科名称转换为中文
table6_long$Discipline <- factor(table6_long$Discipline, levels = c("AL", "CS"), labels = c("应用语言学 (AL)", "计算机科学 (CS)"))
table8_long$Discipline <- factor(table8_long$Discipline, levels = c("AL", "CS"), labels = c("应用语言学 (AL)", "计算机科学 (CS)"))


# --- 4. 开始绘图 ---
# 定义统一的颜色方案和主题
discipline_colors <- c("应用语言学 (AL)" = "#0072B2", "计算机科学 (CS)" = "#D55E00")
# 在主题中指定使用我们加载的字体 "my_font"
common_theme <- theme_classic(base_size = 14) +
  theme(
    text = element_text(family = "my_font"), # 全局应用字体
    plot.title = element_text(hjust = 0.5, face = "bold", size = 16),
    plot.subtitle = element_text(hjust = 0.5, size = 12, color = "gray30"),
    legend.position = "none", # 我们将在最后添加一个统一的图例
    axis.title.x = element_text(face = "bold", margin = margin(t = 10)),
    axis.text = element_text(color = "black")
  )

# 绘制图表6: 句子复杂度
plot_table6 <- ggplot(table6_long, aes(x = Metric, y = Value, fill = Discipline)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(
    aes(label = sprintf("%.2f", Value)), 
    position = position_dodge(width = 0.8), 
    vjust = -0.5, 
    size = 3.5,
    fontface = "bold",
    family = "my_font" # 再次确认字体
  ) +
  scale_fill_manual(values = discipline_colors) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.15))) + # 给顶部的文字留出空间
  labs(
    title = "句子复杂度：AL的宏观优势",
    subtitle = "(源自论文表格6的显著性结果)",
    x = "句法复杂度指标",
    y = "中位数"
  ) +
  common_theme

# 绘制图表8: 名词短语复杂度
plot_table8 <- ggplot(table8_long, aes(x = Metric, y = Value, fill = Discipline)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.7) +
  geom_text(
    aes(label = sprintf("%.2f", Value)), 
    position = position_dodge(width = 0.8), 
    vjust = -0.5, 
    size = 3.5,
    fontface = "bold",
    family = "my_font" # 再次确认字体
  ) +
  scale_fill_manual(values = discipline_colors) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.15))) + # 给顶部的文字留出空间
  labs(
    title = "名词短语复杂度：CS的微观优势",
    subtitle = "(源自论文表格8的显著性结果)",
    x = "名词短语复杂度指标",
    y = "" # 右图不显示y轴标题
  ) +
  common_theme


# --- 5. 合并图表并添加统一图例 ---
final_plot <- plot_table6 + plot_table8 + 
  plot_layout(guides = 'collect') + # 收集所有图例
  plot_annotation(
    title = '跨学科学术摘要语言特征差异分析',
    caption = '数据来源:社会建构主义视角下的跨学科摘要句法差异研究-俞一帆、郭英佳、黄岩',
    theme = theme(
      plot.title = element_text(hjust = 0.5, size = 20, face = "bold", family = "my_font"),
      plot.caption = element_text(color = "gray50", hjust = 1, family = "my_font")
    )
  ) & 
  theme(legend.position = 'top', legend.title = element_blank(), legend.text = element_text(family = "my_font")) # 将图例放在顶部

# 显示最终的图表
print(final_plot)

# 如果需要保存图片到本地，可以取消下面的注释并运行
# ggsave("dichotomy_plot_cn.png", final_plot, width = 14, height = 7, dpi = 300)

