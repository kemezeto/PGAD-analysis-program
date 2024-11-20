import os
import pandas as pd
current_directory = os.getcwd()
csv_files = [file for file in os.listdir(current_directory) if file.endswith('.csv')]

def generate_gene_tree_files(csv_file):
    csv_filename = os.path.splitext(os.path.basename(csv_file))[0]
    
    output_dir = csv_filename
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_file)
    for index, row in df.iterrows():
        gene_name = row['Genetree']
        filename = f"{gene_name}.tree"

        file_content = []
        non_none_count = 0  # 用于统计非 'none' 的基因数

        for col in df.columns[1:]:
            cell_value = row[col]
            if cell_value != 'none':
                non_none_count += 1
                gene_info = cell_value.split('|')
                gene_id = gene_info[0]
                gene_code = gene_info[1]
                col_prefix = col[:3]
                file_content.append(f">{gene_id} {gene_code} {col_prefix}")

        # 如果非 'none' 的基因数量大于1才生成文件
        if non_none_count > 1:
            with open(os.path.join(output_dir, filename), 'w') as f:
                f.write("\n".join(file_content))

def append_gene_sequences_to_tree_files(trees_folder):
    # 缓存所有 .cds 文件的内容
    cds_cache = {}

    for filename in os.listdir(trees_folder):
        if filename.endswith('.tree'):
            tree_file_path = os.path.join(trees_folder, filename)
            print(f"正在处理基因树: {filename}")

            with open(tree_file_path, 'r') as tree_file:
                lines = tree_file.readlines()

            with open(tree_file_path, 'w') as tree_file:
                for line in lines:
                    tree_file.write(line)
                    if line.startswith('>'):
                        parts = line.split()
                        gene_id = parts[0][1:]
                        gene_code = parts[1]
                        last_word = parts[-1]

                        cds_file_name = f"{last_word}.cds"
                        
                        # 如果 .cds 文件还没有被缓存，读取并缓存它的内容
                        if cds_file_name not in cds_cache:
                            if os.path.exists(cds_file_name):
                                gene_sequences = {}
                                with open(cds_file_name, 'r') as cds_file:
                                    current_gene_id = None
                                    current_sequence = []

                                    for cds_line in cds_file:
                                        cds_line = cds_line.strip()
                                        if cds_line.startswith(">"):
                                            if current_gene_id:
                                                gene_sequences[current_gene_id] = ''.join(current_sequence)
                                            current_gene_id = cds_line[1:].split()[0]
                                            current_sequence = []
                                        else:
                                            current_sequence.append(cds_line)
                                    if current_gene_id:
                                        gene_sequences[current_gene_id] = ''.join(current_sequence)
                                
                                # 将读取的 .cds 文件内容缓存起来
                                cds_cache[cds_file_name] = gene_sequences
                            else:
                                # 如果文件不存在，缓存为空字典
                                cds_cache[cds_file_name] = {}

                        # 从缓存中查找基因序列
                        if gene_id in cds_cache.get(cds_file_name, {}):
                            tree_file.write('\n')
                            tree_file.write(cds_cache[cds_file_name][gene_id] + '\n')

                            
def remove_blank_lines_from_tree_files(trees_folder):

    for filename in os.listdir(trees_folder):
        if filename.endswith('.tree'):
            tree_file_path = os.path.join(trees_folder, filename)
            with open(tree_file_path, 'r') as tree_file:
                lines = tree_file.readlines()
            lines = [line for line in lines if line.strip()]
            with open(tree_file_path, 'w') as tree_file:
                tree_file.writelines(lines)

def swap_identifiers_and_names_in_tree_files(trees_folder):
    for filename in os.listdir(trees_folder):
        if filename.endswith('.tree'):
            tree_file_path = os.path.join(trees_folder, filename)

            with open(tree_file_path, 'r') as tree_file:
                lines = tree_file.readlines()
            swapped_lines = []
            for line in lines:
                if line.startswith('>'):
                    parts = line[1:].split(' ', 2)
                    if len(parts) == 3:
                        swapped_line = f">{parts[1]} {parts[0]} {parts[2]}"
                        swapped_lines.append(swapped_line)
                    else:
                        swapped_lines.append(line)
                else:
                    swapped_lines.append(line)
            with open(tree_file_path, 'w') as tree_file:
                tree_file.writelines(swapped_lines)

for csv_file in csv_files:
    print(f"正在处理文件: {csv_file}")
    generate_gene_tree_files(csv_file)
    gene_file_name = csv_file.replace('.csv', '')
    # 生成序列文件
    append_gene_sequences_to_tree_files(gene_file_name)
    # 删除空白行
    remove_blank_lines_from_tree_files(gene_file_name)
    # 交换自定义基因和原始基因位置，可以自己开关
    swap_identifiers_and_names_in_tree_files(gene_file_name)
    