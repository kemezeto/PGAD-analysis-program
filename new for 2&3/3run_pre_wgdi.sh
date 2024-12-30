#!/bin/bash

# 确保 Auto_wgdi 文件夹存在
[ ! -d "Auto_wgdi" ] && mkdir "Auto_wgdi"

# 检查 folder_list.txt 是否存在
if [[ ! -f "folder_list.txt" ]]; then
    echo "错误：folder_list.txt 文件不存在，请确保它存在并包含需要创建文件夹的前缀名称。"
    exit 1
fi

# 读取所有文件名到数组
mapfile -t folder_names < folder_list.txt

# 遍历 folder_list.txt 中的每一个前缀
for folder_name in "${folder_names[@]}"; do
    # 跳过空行
    if [[ -z "$folder_name" ]]; then
        continue
    fi

    # 构建当前 _base 文件夹路径
    base_folder="Auto_wgdi/${folder_name}_base"

    # 确保 _base 文件夹存在
    mkdir -p "$base_folder"

    # 在每个 _base 文件夹中创建子文件夹
    for other_name in "${folder_names[@]}"; do
        # 构建目标文件夹名称（当前 _base 文件夹的前缀 + "_" + 其他文件名）
        sub_folder="${base_folder}/${folder_name}_${other_name}"

        # 创建子文件夹
        mkdir -p "$sub_folder"
        echo "已创建文件夹：$sub_folder"
    done
done


# 遍历 Auto_wgdi 下的所有 _base 文件夹
for base_folder in Auto_wgdi/*_base/; do
    # 获取当前 _base 文件夹的前缀（去掉 Auto_wgdi/ 和 _base）
    base_prefix=${base_folder#Auto_wgdi/}
    base_prefix=${base_prefix%_base}

    echo "正在处理 _base 文件夹：$base_folder"

    # 遍历当前 _base 文件夹中的子文件夹
    for sub_folder in "$base_folder"*/; do
        # 获取子文件夹名称（去掉路径前缀和斜杠）
        sub_folder_name=${sub_folder#$base_folder}
        sub_folder_name=${sub_folder_name%/}

        echo "  正在处理子文件夹：$sub_folder_name"

        # 从子文件夹名称解析出对应的文件夹名称（按 "_" 分割）
        IFS="_" read -r src1 src2 <<< "$sub_folder_name"

        # 检查解析出的文件夹名称是否在 folder_list.txt 中
        for src_folder in "$src1" "$src2"; do
            if [[ " ${folder_names[*]} " =~ " $src_folder " ]]; then
                echo "    复制 $src_folder 文件夹中的文件到 $sub_folder"
                
                # 检查源文件夹是否存在
                if [[ -d "$src_folder" ]]; then
                    # 将源文件夹中的所有文件复制到子文件夹中
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
