import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

# 设置中文字体为黑体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体为SimHei（黑体）
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号显示为方块的问题

# 方法名和颜色
methods = ['scDGCLImpute(ours)', '原始数据', 'DrImpute', 'MAGIC', 'SAVER', 'scImpute', 'GE-Impute', 'CL-Impute']
datasets = ['Baron', 'Usoskin', 'SimData']
metrics = ['ARI', 'NMI']
#colors = plt.cm.tab20(np.arange(len(methods)))
colors = [
    "#629ccc",  # 棕色
    "#eacfd4",  # 红色
    "#f4e8dc",  # 橙色
    "#dab7d7",  # 黄色
    "#e0d5c3",  # 绿色
    "#eeadc1",  # 蓝色
    "#74b2bf",  # 蓝色
    "#c4a5d1",  # 粉色
]

# 初始化数据字典
data_dict = {dataset: {metric: None for metric in metrics} for dataset in datasets}

# 读取CSV文件中的数据
for dataset in datasets:
    filename = f'{dataset}_ARI_NMI.csv'
    df = pd.read_csv(filename, index_col=0)  # 第一列为索引（方法名）
    for metric in metrics:
        data_dict[dataset][metric] = df[metric].values.squeeze()

# Added a gap between different metrics
bar_width = 0.1
gap_width = 0.3
total_width = len(methods) * bar_width + gap_width

fig, axes = plt.subplots(nrows=1, ncols=len(data_dict), figsize=(15, 4), constrained_layout=True)

max_value = 1.02  # 设置y轴的最大值为1.0
for col_idx, (dataset_name, metrics_dict) in enumerate(data_dict.items()):
    ax = axes[col_idx]
    # ax.set_title(dataset_name)
    ax.set_title(dataset_name, fontsize=20, fontweight='bold')  # 设置字体大小为14，加粗
    # 设置y轴的范围以确保1.0包含在内
    ax.set_ylim(0, max_value)

    for metric_idx, metric_name in enumerate(metrics):
        # Offset each group of bars (metric)
        offset = (total_width * metric_idx) - (bar_width * (len(methods) - 1) / 2)
        for method_idx, method in enumerate(methods):
            # Calculate the position of each bar within the group
            position = offset + (method_idx * bar_width)
            ax.bar(position, metrics_dict[metric_name][method_idx], width=bar_width, color=colors[method_idx],
                   label=method if col_idx == 0 and metric_idx == 0 else "")

    # Set x-axis ticks and labels to be in the middle of each group
    ax.set_xticks([total_width * i for i in range(len(metrics))])
    ax.set_xticklabels(metrics)

    if col_idx == 0:
        ax.set_ylabel('')

# 图例
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=len(methods), frameon=False, fontsize=12)

plt.tight_layout(rect=[0, 0.05, 1, 1])

# 保存图像
plt.savefig('plot1.png', format='png', dpi=300)  # 保存为png文件
plt.show()
