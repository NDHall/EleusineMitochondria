#!/bin/bash 

# pipeline to be run after Pipeline.sh



STEM=MP
SL=Val_${STEM}_L_val_1.fq
SR=Val_${STEM}_R_val_2.fq
#~/src_code/trim_galore_zip/trim_galore -a ATACACATCTAGATGTGTATAAGAGACAG -a2 ATACACATCTAGATGTGTATAAGAGACAG --paired --length 90 $SL  $SR
~/src_code/trim_galore_zip/trim_galore -a CATCTAGATGTGTATAAGAGACA -a2 CATCTAGATGTGTATAAGAGACA --paired --length 90 $SL  $SR


SL=Val_${STEM}_L_val_1_val_1.fq
SR=Val_${STEM}_R_val_2_val_2.fq

mv $SR Val2_${STEM}_R.fq
mv $SL Val2_${STEM}_L.fq


fastqc $SL -o qc
fastqc $SR -o qc 

STEM=RD
SL=Val_${STEM}_L.fq
SR=Val_${STEM}_R.fq

~/src_code/trim_galore_zip/trim_galore -a TGATGCTTTCGAACGTCT -a2 TTCGAACCAGGGGTACCG --paired --length 80 $SL  $SR
SL=Val_${STEM}_L_val_1.fq
SR=Val_${STEM}_R_val_2.fq
~/src_code/trim_galore_zip/trim_galore -a TCTACGG  -a2  ACCCGGGGTACCGAAT --paired --length 80 $SL  $SR
SL=Val_${STEM}_L_val_1_val_1.fq
SR=Val_${STEM}_R_val_2_val_2.fq
~/src_code/trim_galore_zip/trim_galore  -a AATACGGAGCTT -a2 AATACGGAGCTT --paired --length 80 $SL  $SR

SL=Val_${STEM}_L_val_1_val_1_val_1.fq
SR=Val_${STEM}_R_val_2_val_2_val_2.fq

mv $SR Val2_${STEM}_R.fq
mv $SL Val2_${STEM}_L.fq
SL=Val2_${STEM}_L.fq
SR=Val2_${STEM}_R.fq

~/src_code/trim_galore_zip/trim_galore  -a  CGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATTCCACACAACAGG -a2 CGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATTCCACACAACAGG  --paired --length 80 $SL  $SR





