#!/bin/bash 

# new pipeline to create cohesive  vector and adapater free read set. 


L=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_L.fastq
R=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_R.fastq

STEM=RD
SL=Val2_${STEM}_L.fq
SR=Val2_${STEM}_R.fq
~/src_code/trim_galore_zip/trim_galore -a TGATGCTTTCGAACGTCT -a2 TTCGAACCAGGGGTACCG --paired --length 75 $SL  $SR
