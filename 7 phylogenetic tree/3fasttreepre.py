import os
import subprocess

def process_tree_files(trees_folder):
    output_folder = f"{trees_folder}_nwk"
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(trees_folder):
        if filename.endswith('.fasta'):
            print(f"正在处理{filename}。")
            tree_file_path = os.path.join(trees_folder, filename)
            output_file_name = filename.replace('.fasta', '.nwk')
            output_file_path = os.path.join(output_folder, output_file_name)

            # 执行mafft命令
            command = f"FastTree -gtr -nt {tree_file_path} > {output_file_path}"
            # command = f"FastTree -jc -nt {tree_file_path} > {output_file_path}"
            subprocess.run(command, shell=True)

    print(f"所有.tree文件已处理完毕。")
    
Chr = 11
# 遍历从1到11的染色体号
for i in range(1, Chr + 1):
    process_tree_files(f'Acoraceae_Agr_chr{i}_mafft')