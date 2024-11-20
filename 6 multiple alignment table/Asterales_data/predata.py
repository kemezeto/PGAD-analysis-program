import os
import pandas as pd

# 获取当前目录下所有.csv文件
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

# 遍历所有.csv文件
for csv_file in csv_files:
    csv_file_path = csv_file

    # 使用 pandas 读取 csv 文件，并将第一行作为列名
    block_df = pd.read_csv(csv_file_path, header=0)  # 假设第一行是列名

    # 获取文件名（不包括扩展名）
    file_name = os.path.splitext(csv_file)[0]

    # 生成 Genetree 列的内容
    block_df['Genetree'] = [f"{file_name}_gene" + str(i+1) for i in block_df.index]

    # 将 Genetree 列移动到第一列
    block_df.insert(0, 'Genetree', block_df.pop('Genetree'))
    block_df.to_csv(csv_file, index=False, header=True)
    print(csv_file + "is ok")