#!/bin/bash

for pep_folder in Auto_pep/*_pep/; do
    species_name=${pep_folder#Auto_pep/}
    species_name=${species_name%_pep/}

    echo "正在处理物种：$species_name"

    # 遍历 _pep 文件夹下的所有 .blast 文件
    for blast_file in "$pep_folder"/*.blast; do
        # 检查是否有 .blast 文件
        if [[ -f "$blast_file" ]]; then
            # 获取 .blast 文件的文件名
            blast_filename=$(basename "$blast_file")
            
            # 去掉 .blast 后缀，获取目标文件夹名称（如 Ama_Ama）
            target_folder_name=${blast_filename%.blast}

            # 构建正确的目标文件夹路径
            target_folder="Auto_wgdi/${species_name}_base/${target_folder_name}"

            # 打印调试信息，检查目标路径
            echo "  检查目标文件夹：$target_folder"

            # 检查目标文件夹是否存在
            if [[ -d "$target_folder" ]]; then
                # 移动 .blast 文件到目标文件夹
                mv "$blast_file" "$target_folder/"
                echo "  已移动 $blast_file 到 $target_folder/"
            else
                echo "  警告：目标文件夹 $target_folder 不存在，跳过 $blast_file"
            fi
        else
            echo "  警告：未找到 .blast 文件，跳过 $pep_folder"
        fi
    done
done

echo "所有操作已完成！"
