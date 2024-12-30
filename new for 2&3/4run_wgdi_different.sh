#!/bin/bash

# 遍历 Auto_wgdi 下的所有 _base 文件夹
for base_folder in Auto_wgdi/*_base/; do
    echo "正在处理 _base 文件夹：$base_folder"

    # 遍历 _base 文件夹中的子文件夹
    for sub_folder in "$base_folder"*/; do
        # 获取子文件夹名称
        sub_folder_name=${sub_folder#$base_folder}
        sub_folder_name=${sub_folder_name%/}

        # 检查是否是不同物种的文件夹（如 Jmi_Tgr）
        IFS="_" read -r species1 species2 <<< "$sub_folder_name"
        if [[ "$species1" != "$species2" ]]; then
            echo "  发现不同物种对比文件夹：$sub_folder_name，生成配置文件。"

            # 生成 run.sh 文件
            cat > "$sub_folder/run.sh" <<EOL
cat $species1.cds >> all.cds
cat $species2.cds >> all.cds
cat $species1.pep >> all.pep
cat $species2.pep >> all.pep
wgdi -d total.conf
wgdi -icl total.conf
wgdi -ks total.conf
wgdi -bi total.conf
wgdi -bk total.conf
wgdi -kp total.conf
wgdi -pf total.conf
EOL

            echo "    生成文件：$sub_folder/run.sh"

            # 生成 total.conf 文件
            cat > "$sub_folder/total.conf" <<EOL
[dotplot]
blast = ${species1}_${species2}.blast
gff1 = $species1.new.gff
gff2 = $species2.new.gff
lens1 = $species1.lens
lens2 = $species2.lens
genome1_name = $species1
genome2_name = $species2
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
savefig = ${species1}_${species2}.png

[collinearity]
blast = ${species1}_${species2}.blast
gff1 = $species1.new.gff
gff2 = $species2.new.gff
lens1 = $species1.lens
lens2 = $species2.lens
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
savefile = ${species1}_${species2}.icl

[ks]
cds_file = all.cds
pep_file = all.pep
align_software = muscle
pairs_file = ${species1}_${species2}.icl
ks_file = ${species1}_${species2}.ks

[blockinfo]
blast = ${species1}_${species2}.blast
gff1 = $species1.new.gff
gff2 = $species2.new.gff
lens1 = $species1.lens
lens2 = $species2.lens
collinearity = ${species1}_${species2}.icl
score = 100
evalue = 1e-5
repeat_number = 20
position = order
ks = ${species1}_${species2}.ks
ks_col = ks_NG86
savefile = ${species1}_${species2}.bi.csv

[blockks]
lens1 = $species1.lens
lens2 = $species2.lens
genome1_name = $species1
genome2_name = $species2
blockinfo = ${species1}_${species2}.bi.csv
pvalue = 0.2
tandem = true
tandem_length = 200
markersize = 1
area = 0,2
block_length = 5
figsize = 8,8
savefig = ${species1}_${species2}.bk.png

[kspeaks]
blockinfo = ${species1}_${species2}.bi.csv
pvalue = 0.2
tandem = true
block_length = 5
ks_area = 0,10
multiple = 1
homo = 0,1
fontsize = 9
area = 0,3
figsize = 10,6.18
savefig = ${species1}_${species2}.kp.png
savefile = ${species1}_${species2}.kp

[peaksfit]
blockinfo = ${species1}_${species2}.bi.csv
mode = median
bins_number = 200
ks_area = 0,10
fontsize = 9
area = 0,3
figsize = 10,6.18
shadow = true
savefig = ${species1}_${species2}.pf.png

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
savefig = ${species1}_${species2}.kf.png
EOL

            echo "    生成文件：$sub_folder/total.conf"
        else
            echo "  跳过一致文件夹：$sub_folder_name"
        fi
    done
done

echo "所有操作已完成！"
