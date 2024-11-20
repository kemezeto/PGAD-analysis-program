import pandas as pd
import numpy as np
merged = pd.read_csv('./merged_output_new.csv')
# 读取CSV文件
fenzu = pd.read_csv('./fenzu.csv', header=None, sep=',')

# 初始化一个空列表，用于存储"color"列的数据
color_list = []

# 遍历数据框的每一行
for index, row in fenzu.iterrows():
    # 从行数据中提取第二个元素（列索引为1），得到重复次数
    count_start = row[0]
    count = row[1]
    # 从行数据中提取第三个元素（列索引为2），作为颜色名称
    color_name = row[2]
    # 将颜色名称重复count次，形成字符串，并添加到color_list列表中
    repeated_color = (color_name + ' ') * (count - count_start + 1)
    # 将重复后的字符串分割成单独的元素，然后添加到列表中
    color_list.extend(repeated_color.split())

# 创建一个新的数据框，每行包含一个颜色名称
chr_color = pd.DataFrame({'color': color_list})
print('分组文件：', len(chr_color), '多重比对文件：', len(merged))

# 定义一个函数，使用正则表达式分割字符串
import re
def split_chr(s):
    # 使用正则表达式匹配一个或多个字母，后跟一个或多个数字
    pattern = re.compile(r'([A-Za-z]+)([0-9]+)([A-Za-z]+)([0-9]+)')
    chr = pattern.findall(s)[0][1]
    # gene_num = pattern.findall(s)[0][3]
    chr = int(chr)
    return chr
def split_gene(s):
    # 使用正则表达式匹配一个或多个字母，后跟一个或多个数字
    pattern = re.compile(r'([A-Za-z]+)([0-9]+)([A-Za-z]+)([0-9]+)')
    # chr = pattern.findall(s)[0][1]
    gene_num = pattern.findall(s)[0][3]
    gene_num = int(gene_num)
    return gene_num
# 应用函数到'reference1'列，并创建新列'split_reference1'
merged['chr'] = merged['reference1'].apply(split_chr)
merged['gene'] = merged['reference1'].apply(split_gene)

def create_fenzu(row):
    return f"{row['chr'] - 1}={row['gene']}"

# 应用这个函数到每一行，创建新的fenzu列
merged['fenzu'] = merged.apply(create_fenzu, axis=1)
merged.drop(['chr', 'gene'], axis=1, inplace=True)
merged['color'] = chr_color['color'].values

columns = merged.columns.tolist()
columns = ['fenzu','color'] + [col for col in columns if col not in ['fenzu','color']]
# 最后，使用reindex方法重新排列列的顺序
merged = merged.reindex(columns=columns)

clo_num = len(merged.columns)
# 计算需要添加的空白列数
blank_cols_to_add = 30 - clo_num
# 创建一个空白列的DataFrame，每列的值都设置为NaN（表示缺失值）
blank_cols = pd.DataFrame(np.full((merged.shape[0], blank_cols_to_add), np.nan))
# 将空白列添加到merged的最后
merged = pd.concat([merged, blank_cols], axis=1)
merged.fillna('.', inplace=True)

merged.to_csv('output_new.csv', sep='\t', index=False, header=False)