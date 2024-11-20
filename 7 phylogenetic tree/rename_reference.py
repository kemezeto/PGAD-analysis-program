import os
import pandas as pd

# 获取当前目录下所有.csv文件
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

# 遍历所有.csv文件
for csv_file in csv_files:
    csv_file_path = csv_file

    # 使用 pandas 读取 csv 文件，并将第一行作为列名
    block_df = pd.read_csv(csv_file_path, header=0)  # 假设第一行是列名
    block_df.rename(columns={'reference1': 'Mac_a'}, inplace=True)

    block_df.to_csv(csv_file, index=False, header=True)
    print(csv_file + " is ok")