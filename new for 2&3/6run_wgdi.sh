#!/bin/bash

# 遍历 Auto_wgdi 目录下的所有 _base 文件夹
for base_folder in Auto_wgdi/*_base/; do
    echo "正在处理 _base 文件夹：$base_folder"

    # 遍历 _base 文件夹下的所有子文件夹
    for sub_folder in "$base_folder"*/; do
        # 检查子文件夹中是否存在 run.sh
        if [[ -f "$sub_folder/run.sh" ]]; then
            echo "  发现 run.sh 脚本，正在执行：$sub_folder/run.sh"
            
            # 进入子文件夹并执行 run.sh
            cd "$sub_folder" || {
                echo "  错误：无法进入文件夹 $sub_folder，跳过。"
                continue
            }

            bash run.sh

            # 返回到上一级目录
            cd - > /dev/null
        else
            echo "  未发现 run.sh 脚本，跳过文件夹：$sub_folder"
        fi
    done
done

echo "所有操作已完成！"
