#!/bin/bash

# 检查 all.bed 文件是否存在，如果不存在则创建
[ ! -f all.bed ] && touch all.bed

# 遍历当前目录下所有 .new.gff 结尾的文件
for file in *.new.gff
do
    # 将每个文件的内容追加到 all.bed
    cat "$file" >> all.bed
done