#!/bin/bash

[ ! -d "Auto_wgdi" ] && mkdir "Auto_wgdi"

if [[ ! -f "folder_list.txt" ]]; then
    echo "错误：folder_list.txt 文件不存在，请确保它存在并包含需要创建文件夹的前缀名称。"
    exit 1
fi

mapfile -t folder_names < folder_list.txt

for folder_name in "${folder_names[@]}"; do

    if [[ -z "$folder_name" ]]; then
        continue
    fi

    base_folder="Auto_wgdi/${folder_name}_base"


    mkdir -p "$base_folder"


    for other_name in "${folder_names[@]}"; do

        sub_folder="${base_folder}/${folder_name}_${other_name}"


        mkdir -p "$sub_folder"
        echo "已创建文件夹：$sub_folder"
    done
done



for base_folder in Auto_wgdi/*_base/; do

    base_prefix=${base_folder#Auto_wgdi/}
    base_prefix=${base_prefix%_base}

    echo "正在处理 _base 文件夹：$base_folder"


    for sub_folder in "$base_folder"*/; do

        sub_folder_name=${sub_folder#$base_folder}
        sub_folder_name=${sub_folder_name%/}

        echo "  正在处理子文件夹：$sub_folder_name"


        IFS="_" read -r src1 src2 <<< "$sub_folder_name"


        for src_folder in "$src1" "$src2"; do
            if [[ " ${folder_names[*]} " =~ " $src_folder " ]]; then
                echo "    复制 $src_folder 文件夹中的文件到 $sub_folder"
                

                if [[ -d "$src_folder" ]]; then

                    cp -r "$src_folder"/* "$sub_folder/"
                else
                    echo "    错误：源文件夹 $src_folder 不存在，跳过。"
                fi
            else
                echo "    错误：文件夹 $src_folder 不在 folder_list.txt 中，跳过。"
            fi
        done
    done
done

echo "所有操作已完成！"
