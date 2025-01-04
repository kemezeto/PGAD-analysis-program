#!/bin/bash

blastp_path="blast_path/run_blastp/blast+/bin/blastp"
makeblastdb_path="blast_path/run_blastp/blast+/bin/makeblastdb"

[ ! -d "Auto_pep" ] && mkdir "Auto_pep"
[ ! -d "Auto_wgdi" ] && mkdir "Auto_wgdi"

output_file="folder_list.txt"
> "$output_file"

pep_files=()

for folder in */; do
    folder_name=${folder%/}
    
    if [[ $folder_name != Auto_* ]]; then
        echo "$folder_name" >> "$output_file"
        
        mkdir -p "Auto_pep/${folder_name}_pep"

        for pep_file in "$folder_name"/*.pep; do
            if [[ -f $pep_file ]]; then
                pep_files+=("$pep_file")
            fi
        done
    fi
done

if [[ ${#pep_files[@]} -eq 0 ]]; then
    echo "未找到任何 .pep 文件，操作结束。"
    exit 0
fi

for folder in Auto_pep/*_pep/; do
    for pep_file in "${pep_files[@]}"; do
        cp "$pep_file" "$folder"
    done
done

for folder in Auto_pep/*_pep/; do
    species_name=${folder#Auto_pep/}
    species_name=${species_name%_pep/}

    echo "进入文件夹：$folder"
    cd "$folder" || exit

	for i in *.pep; do
		echo "处理文件：$i"

		file_base_name=${i%.pep}
		
		echo "基准物种：$species_name 比对物种： $file_base_name"
		
		$makeblastdb_path -in "$i" -dbtype prot -out "$i.db"
		
		$blastp_path -query "$species_name.pep" -db "$i.db" -out "${species_name}_${file_base_name}.blast" -outfmt 6 -evalue 1e-5 -max_target_seqs 20 -num_threads 4
	done
	
    cd - > /dev/null
done

echo "所有操作已完成！"
