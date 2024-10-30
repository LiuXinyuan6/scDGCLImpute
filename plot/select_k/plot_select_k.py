import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置中文字体，尝试使用 SimHei 字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体为 SimHei（黑体）  SimSun(宋体）
# # 设置全局字体大小
# plt.rcParams.update({'font.size': 40})  # 设置全局字体大小，例如14
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题



# 画 ARI 和 NMI
# # 用于 Baron、Usoskin、SimData数据集
# 使用嵌套元组输入数据 (K, ARI, NMI)

# SimData
data = [
    (1, 0.92261, 0.94570),
    (5, 0.92454, 0.95521),
    (10, 0.99952, 0.99882),
    (15, 0.91896, 0.94871),
    (20, 0.91526, 0.94975)
]


# 提取 K 值, ARI 值和 NMI 值
K_values = [item[0] for item in data]
ARI_values = [item[1] for item in data]
NMI_values = [item[2] for item in data]

# 创建图表
plt.figure(figsize=(25, 15))

# 画ARI的折线图，点为方块，跳过 None 值
plt.plot([k for k, ari in zip(K_values, ARI_values) if ari is not None],
         [ari for ari in ARI_values if ari is not None],
         marker='s', color='b', label='ARI', linewidth=6, markersize=20)

# 画NMI的折线图，点为星星，跳过 None 值
plt.plot([k for k, nmi in zip(K_values, NMI_values) if nmi is not None],
         [nmi for nmi in NMI_values if nmi is not None],
         marker='*', color='r', label='NMI', linewidth=6, markersize=20)

# 添加图例
plt.legend(fontsize=30)  # 调整图例字体大小

# 添加标题和轴标签
plt.title('SimData', fontsize=70)
plt.xlabel('K', fontsize=60)
plt.ylabel('ARI and NMI', fontsize=60)

# 设置横坐标刻度为指定值
xticks_values = [0, 1, 5, 10, 15]  # 自定义刻度值
plt.xticks(xticks_values, fontsize=50)
plt.yticks(fontsize=50)

# 保存为高清图片
plt.savefig('2_SimData_plot_select_k.png', dpi=300)  # dpi=300 是高清标准

# 显示图表
plt.show()



# # 画 PCC、 L1 和 RMSE
# # 用于 Pbmc、Jurkat-293t数据集
# # 使用嵌套元组输入数据 (K, PCC, L1、RMSE)
#
# # Pbmc
# data = [
#     (1, 0.78573, 0.14399, 3.19568),
#     (5, 0.78668, 0.14314, 3.18920),
#     (10, 0.78879, 0.14273, 3.17454),
#     (15, 0.78892, 0.14276, 3.17396),
#     (20, 0.78410, 0.14291, 3.21076),
#     (25, 0.78525, 0.14321, 3.20157)
# ]
#
#
# # 提取 K 值, PCC、L1和 RMSE 值
# K_values = [item[0] for item in data]
# PCC_values = [item[1] for item in data]
# L1_values = [item[2] for item in data]
# RMSE_values = [item[3] for item in data]
#
# # 创建图表
# plt.figure(figsize=(25, 15))
#
# # 画PCC的折线图，点为方块，跳过 None 值
# plt.plot([k for k, pcc in zip(K_values, PCC_values) if pcc is not None],
#          [pcc for pcc in PCC_values if pcc is not None],
#          marker='s', color='b', label='PCC', linewidth=6, markersize=20)
#
# # 画L1的折线图，点为星星，跳过 None 值
# plt.plot([k for k, L1 in zip(K_values, L1_values) if L1 is not None],
#          [L1 for L1 in L1_values if L1 is not None],
#          marker='*', color='r', label='L1', linewidth=6, markersize=20)
#
# # 画RMSE的折线图，点为星星，跳过 None 值
# plt.plot([k for k, RMSE in zip(K_values, RMSE_values) if RMSE is not None],
#          [RMSE for RMSE in RMSE_values if RMSE is not None],
#          marker='^', color='g', label='RMSE', linewidth=6, markersize=20)
#
# # 添加图例
# plt.legend(fontsize=30)  # 调整图例字体大小
#
# # 添加标题和轴标签
# plt.title('Pbmc', fontsize=70)
# plt.xlabel('K', fontsize=60)
# plt.ylabel('PCC、L1 and RMSE', fontsize=60)
#
# # 设置横坐标刻度为指定值
# xticks_values = [0, 1, 5, 10, 15, 20, 25]  # 自定义刻度值
# plt.xticks(xticks_values, fontsize=50)
# plt.yticks(fontsize=50)
#
# # 保存为高清图片
# plt.savefig('2_Pbmc_plot_select_k.png', dpi=300)  # dpi=300 是高清标准
#
# # 显示图表
# plt.show()






# 各数据集参数信息

# 使用ARI、NMI衡量的数据集

# Baron
# data = [
#     (1, 0.51232, 0.76271),
#     (5, 0.46694, 0.74168),
#     (10, 0.50379, 0.76061),
#     (15, 0.56608, 0.78716),
#     (20, 0.50864, 0.76290),
#     (25, 0.63389, 0.80128),
#     (30, 0.56284, 0.77199),
#     (35, 0.51265, 0.76316)
# ]

# Usoskin
# data = [
#     (1, 0.91974, 0.87625),
#     (5, 0.95186, 0.92254),
#     (10, 0.91456, 0.86719),
#     (15, 0.89256, 0.84106)
# ]

# SimData
# data = [
#     (1, 0.92261, 0.94570),
#     (5, 0.92454, 0.95521),
#     (10, 0.99952, 0.99882),
#     (15, 0.91896, 0.94871),
#     (20, 0.91526, 0.94975)
# ]

# 使用PCC、L1、RMSE衡量的数据集

# Pbmc
# data = [
#     (1, 0.78573, 0.14399, 3.19568),
#     (5, 0.78668, 0.14314, 3.18920),
#     (10, 0.78879, 0.14273, 3.17454),
#     (15, 0.78892, 0.14276, 3.17396),
#     (20, 0.78410, 0.14291, 3.21076),
#     (25, 0.78525, 0.14321, 3.20157)
# ]

# Jurkat-293t
# data = [
#     (1, 0.95430, 0.38087, 2.64145),
#     (5, 0.95500, 0.38161, 2.62145),
#     (10, 0.95583, 0.38118, 2.59781),
#     (15, 0.95493, 0.38152, 2.62378),
#     (20, 0.95496, 0.38173, 2.62300),
#     (25, 0.95568, 0.38231, 2.60258)
# ]