#!/bin/bash

# 遍历 Auto_wgdi 下的所有 _base 文件夹
for base_folder in Auto_wgdi/*_base/; do
    echo "正在处理 _base 文件夹：$base_folder"

    # 遍历 _base 文件夹中的子文件夹
    for sub_folder in "$base_folder"*/; do
        # 获取子文件夹名称
        sub_folder_name=${sub_folder#$base_folder}
        sub_folder_name=${sub_folder_name%/}

        # 检查是否是前后一致的子文件夹（如 Jmi_Jmi）
        IFS="_" read -r prefix1 prefix2 <<< "$sub_folder_name"
        if [[ "$prefix1" == "$prefix2" ]]; then
            echo "  发现一致文件夹：$sub_folder_name，生成配置文件。"

            # 物种名称为前缀（如 Jmi）
            species_name=$prefix1

            # 生成 run.sh 文件
            cat > "$sub_folder/run.sh" <<EOL
wgdi -d total.conf
wgdi -icl total.conf
wgdi -ks total.conf
wgdi -bi total.conf
wgdi -c total.conf
wgdi -bk total.conf
wgdi -kp total.conf
wgdi -pf total.conf
EOL

            echo "    生成文件：$sub_folder/run.sh"

            # 生成 total.conf 文件
            cat > "$sub_folder/total.conf" <<EOL
[dotplot]
blast = $species_name.blast
gff1 = $species_name.new.gff
gff2 = $species_name.new.gff
lens1 = $species_name.lens
lens2 = $species_name.lens
genome1_name = $species_name
genome2_name = $species_name
multiple = 1
score = 100
evalue = 1e-5
repeat_number = 10
position = order
blast_reverse = false
ancestor_left = none
ancestor_top = none
markersize = 0.5
figsize = 10,10
savefig = $species_name.png

[collinearity]
blast = $species_name.blast
gff1 = $species_name.new.gff
gff2 = $species_name.new.gff
lens1 = $species_name.lens
lens2 = $species_name.lens
blast_reverse = false
multiple = 1
process = 8
evalue = 1e-5
score = 100
grading = 50,25,10
mg = 25,25
pvalue = 1
repeat_number = 10
positon = order
savefile = $species_name.icl

[ks]
cds_file = $species_name.cds
pep_file = $species_name.pep
align_software = muscle
pairs_file = $species_name.icl
ks_file = $species_name.ks

[blockinfo]
blast = $species_name.blast
gff1 = $species_name.new.gff
gff2 = $species_name.new.gff
lens1 = $species_name.lens
lens2 = $species_name.lens
collinearity = $species_name.icl
score = 100
evalue = 1e-5
repeat_number = 20
position = order
ks = $species_name.ks
ks_col = ks_NG86
savefile = $species_name.bi.csv

[correspondence]
blockinfo = $species_name.bi.csv
lens1 = $species_name.lens
lens2 = $species_name.lens
tandem = true
tandem_length = 200
pvalue = 0.2
block_length = 5
tandem_ratio = 0.5
multiple = 1
homo = -1,1
savefile = $species_name.bi.c.csv

[blockks]
lens1 = $species_name.lens
lens2 = $species_name.lens
genome1_name = $species_name
genome2_name = $species_name
blockinfo = $species_name.bi.csv
pvalue = 0.2
tandem = true
tandem_length = 200
markersize = 1
area = 0,2
block_length = 5
figsize = 8,8
savefig = $species_name.bk.png

[kspeaks]
blockinfo = $species_name.bi.csv
pvalue = 0.2
tandem = true
block_length = 5
ks_area = 0,10
multiple = 1
homo = 0,1
fontsize = 9
area = 0,3
figsize = 10,6.18
savefig = $species_name.kp.png
savefile = $species_name.kp

[peaksfit]
blockinfo = $species_name.bi.csv
mode = median
bins_number = 200
ks_area = 0,10
fontsize = 9
area = 0,3
figsize = 10,6.18
shadow = true
savefig = $species_name.pf.png

[ksfigure]
ksfit = ks_fit_result.csv
labelfontsize = 15
legendfontsize = 15
xlabel = none
ylabel = none
title = none
area = 0,2
figsize = 10,6.18
shadow = false
savefig = $species_name.kf.png
EOL

            echo "    生成文件：$sub_folder/total.conf"
        else
            echo "  跳过非一致文件夹：$sub_folder_name"
        fi
    done
done

echo "所有操作已完成！"
