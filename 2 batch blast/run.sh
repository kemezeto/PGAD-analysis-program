#!/bin/bash
blastp_path="/run_blastp/blast+/bin/blastp"
makeblastdb_path="/run_blastp/blast+/bin/makeblastdb"

for i in *.pep; do
  echo $i
  $makeblastdb_path -in $i -dbtype prot -out $i.db
  $blastp_path -query Bni.pep -db $i.db -out $i.Bni.blast -outfmt 6 -evalue 1e-5 -max_target_seqs 20 -num_threads 4
done
