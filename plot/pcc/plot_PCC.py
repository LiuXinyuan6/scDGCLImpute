import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置中文字体为黑体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体为SimHei（黑体）

# 方法名和颜色
methods = ['scDGCLImpute(ours)', 'raw', 'DrImpute', 'MAGIC', 'SAVER', 'scImpute', 'GE-Impute', 'CL-Impute']
datasets = ['Pbmc', 'Juraket-293t', 'SimData']
dropouts = {'Pbmc': ['30', '40', '50'],
            'Juraket-293t': ['30', '40', '50'],
            'SimData': ['30', '40', '50', '65', '80']}
metrics = ['PCC', 'L1', 'RMSE']  # 只包含PCC

colors = [
    "#629ccc",
    "#eacfd4",
    "#f4e8dc",
    "#dab7d7",
    "#e0d5c3",
    "#eeadc1",
    "#74b2bf",
    "#c4a5d1",
]
dropout_labels = ['dropout 20%', 'dropout 40%', 'dropout 60%']

# 初始化数据字典
data_dict = {dataset: {metric: {dropout: None for dropout in dropouts} for metric in metrics} for dataset in datasets}

# 读取CSV文件中的数据
for dataset in datasets:
    for dropout in dropouts[dataset]:
        for metric in metrics:
            filename = f'{dataset}_dropout_{dropout}_{metric}.csv'
            df = pd.read_csv(filename, index_col=0)
            data_dict[dataset][metric][dropout] = df.values.squeeze()


# Added a gap between different dropout percentages
bar_width = 0.1
gap_width = 0.3
total_width = len(methods) * bar_width + gap_width

# 设置方法名显示
method_display_names = {
    'raw': '缺失数据',
    'scDGCLImpute(ours)': 'scDGCLImpute(ours)',
    'DrImpute': 'DrImpute',
    'MAGIC': 'MAGIC',
    'SAVER': 'SAVER',
    'scImpute': 'scImpute',
    'GE-Impute': 'GE-Impute',
    'CL-Impute': 'CL-Impute'
}

# 修改数据集名称显示
dataset_display_names = {
    'Pbmc': 'Pbmc',
    'Juraket-293t': 'Jurkat-293t',  # 修正拼写错误
    'SimData': 'SimData'
}

# 设置中文字体为黑体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 设置子图并添加调整
fig, axes = plt.subplots(
    nrows=3,
    ncols=len(data_dict),
    figsize=(18, 12),
    constrained_layout=True,
    gridspec_kw={'width_ratios': [1, 1, 1.5]}  # 设置第三列的宽度比例更大
)

for col_idx, (dataset_name, metrics_dict) in enumerate(data_dict.items()):
    for row_idx, (metric_name, dropout_values_dict) in enumerate(metrics_dict.items()):
        ax = axes[row_idx, col_idx]
        display_dataset_name = dataset_display_names.get(dataset_name, dataset_name)  # 获取修正后的数据集名称
        if row_idx == 0:
            ax.set_title(display_dataset_name, fontsize=20, fontweight='bold')

        if col_idx == 0:
            ax.set_ylabel(metric_name, fontsize=16)
        else:
            ax.set_ylabel('')

        for dropout_idx, dropout in enumerate(dropouts[dataset_name]):
            dropout_label = f'dropout {dropout}%'
            offset = (total_width * dropout_idx) - (bar_width * (len(methods) - 1) / 2)
            for method_idx, method in enumerate(methods):
                display_method_name = method_display_names.get(method, method)  # 获取修正后的方法名称
                position = offset + (method_idx * bar_width)
                ax.bar(position, dropout_values_dict[dropout][method_idx], width=bar_width, color=colors[method_idx],
                       label=display_method_name if col_idx == 0 and dropout_idx == 0 else "")

        ax.set_xticks([total_width * i for i in range(len(dropouts[dataset_name]))])
        ax.set_xticklabels([f'缺失率 {d}%' for d in dropouts[dataset_name]], fontsize=12)

# 获取第一行第一列子图中的图例句柄和标签
handles, labels = axes[0, 0].get_legend_handles_labels()
# 在图形对象中添加图例，置于底部中央，没有边框
fig.legend(handles, labels, loc='lower center', ncol=len(methods), frameon=False, fontsize=12)

# 调整子图的布局
plt.tight_layout(rect=[0, 0.05, 1, 1])

# 保存为png文件
plt.savefig('2_plot.png', format='png', dpi=300)
plt.show()