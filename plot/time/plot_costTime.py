import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体为黑体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体为SimHei（黑体）


# 读取CSV文件
df = pd.read_csv('cost_time.csv')

# 获取方法名称和数据集名称
methods = df.iloc[1:, 0].values  # 第一列，从第二行到最后一行是方法名
datasets = df.columns[1:]  # 第一行，从第二列到最后一列是数据集名

# 获取运行时间数据
runtime_data = df.iloc[1:, 1:].values  # 排除第一行第一列的内容，取数值部分

# 定义颜色
colors = [
    "#629ccc",
    "#eacfd4",
    "#f4e8dc",
    "#dab7d7",
    "#e0d5c3",
    "#eeadc1",
    "#74b2bf",
    "#c4a5d1",
    "#7d7fb0",
]

# 创建图形对象和子图axes
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制柱状图
bar_width = 0.1
for i, method in enumerate(methods):
    ax.bar([x + i * bar_width for x in range(len(datasets))], runtime_data[i],
           width=bar_width, color=colors[i % len(colors)], label=method)

# 设置y轴为对数刻度
ax.set_yscale('log')

# 设置x轴刻度位置和标签
ax.set_xticks([x + bar_width * (len(methods) - 1) / 2 for x in range(len(datasets))])
ax.set_xticklabels(datasets, fontsize=12)

# 设置y轴标签
ax.set_ylabel('运行时间(s)', fontsize=14)
ax.set_xlabel('数据集', fontsize=14)

# 添加图例
ax.legend(title='方法', loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=len(methods), fontsize=8)

# 添加标题
ax.set_title('不同方法和数据集的运行时间对比', fontsize=16, fontweight='bold')

# 调整布局以适应图例
plt.tight_layout()

# 保存图像
plt.savefig('1_runtime_comparison.png', format='png', dpi=300)

# 显示图形
plt.show()