#!/bin/bash 

# pipeline to be run after Pipeline_II.sh


L=Val2_MP_L.fq
R=Val2_MP_R.fq
~/src_code/trim_galore_zip/trim_galore -a CATCTAGATGTGTATAAGAGACA -a2 CATCTAGATGTGTATAAGAGACA --paired  $SL  $SR  --length 75 $L  $R

fastqc Val2_MP_L_val_1.fq -o qc
fastqc Val2_MP_R_val_2.fq -o qc

# highest problem Kmers were occuring in biologically real Seqs. Spotchecking suggests this is just a function of bias or very high sequence repeats.

