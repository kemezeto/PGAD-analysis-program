#!/bin/bash

# 定义路径
blastp_path="filepath/run_blastp/blast+/bin/blastp"
makeblastdb_path="filepath/run_blastp/blast+/bin/makeblastdb"

# 创建 Auto_pep 和 Auto_wgdi 文件夹（如果不存在）
[ ! -d "Auto_pep" ] && mkdir "Auto_pep"
[ ! -d "Auto_wgdi" ] && mkdir "Auto_wgdi"

# 文件记录输出文件
output_file="folder_list.txt"
> "$output_file"  # 清空文件内容（如果存在）

# 临时存储所有 .pep 文件路径的数组
pep_files=()

# 遍历当前目录下的所有文件夹
for folder in */; do
    # 去除最后的斜杠，获取文件夹名称
    folder_name=${folder%/}
    
    # 检查文件夹是否以 Auto_ 开头
    if [[ $folder_name != Auto_* ]]; then
        echo "$folder_name" >> "$output_file"  # 记录文件夹名称到文件中
        
        # 在 Auto_pep 文件夹里创建对应的文件夹
        mkdir -p "Auto_pep/${folder_name}_pep"

        # 搜索 .pep 文件并存储到数组中
        for pep_file in "$folder_name"/*.pep; do
            if [[ -f $pep_file ]]; then
                pep_files+=("$pep_file")  # 添加到数组
            fi
        done
    fi
done

# 检查是否有 .pep 文件
if [[ ${#pep_files[@]} -eq 0 ]]; then
    echo "未找到任何 .pep 文件，操作结束。"
    exit 0
fi

# 将所有 .pep 文件复制到每个 _pep 文件夹中
for folder in Auto_pep/*_pep/; do
    for pep_file in "${pep_files[@]}"; do
        cp "$pep_file" "$folder"  # 复制文件
    done
done

# 遍历每个 _pep 文件夹并执行指定脚本
for folder in Auto_pep/*_pep/; do
    # 获取物种名称（去掉 _pep 后缀）
    species_name=${folder#Auto_pep/}
    species_name=${species_name%_pep/}

    echo "进入文件夹：$folder"
    cd "$folder" || exit  # 进入 _pep 文件夹

    # 对每个 .pep 文件执行脚本
	# 对每个 .pep 文件执行脚本
	for i in *.pep; do
		echo "处理文件：$i"
		
		# 去掉 .pep 后缀
		file_base_name=${i%.pep}
		
		echo "基准物种：$species_name 比对物种： $file_base_name"
		
		# 创建数据库
		$makeblastdb_path -in "$i" -dbtype prot -out "$i.db"
		
		# 执行 blastp，并修改输出文件名为 species_name_file_base_name.blast
		$blastp_path -query "$species_name.pep" -db "$i.db" -out "${species_name}_${file_base_name}.blast" -outfmt 6 -evalue 1e-5 -max_target_seqs 20 -num_threads 4
	done
	
    cd - > /dev/null  # 返回上一级目录
done

echo "所有操作已完成！"
