#!/bin/bash 

# new pipeline to create cohesive  vector and adapater free read set. 


L=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_L.fastq
R=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_R.fastq

STEM=RD


 ./Vector_filter.sh $L $R $STEM >>output.txt
# FV for free of vector, OPtimistic... yes. But this should take care of a lot of the underlying contamination.
SL=${STEM}_FV_L.fq
SR=${STEM}_FV_R.fq


~/src_code/trim_galore_zip/trim_galore --paired --illumina  --clip_R2 15 --length 75 $SL  $SR  >>output.txt

SL=${STEM}_FV_L_val_1.fq
SR=${STEM}_FV_R_val_2.fq


~/src_code/trim_galore_zip/trim_galore --paired --adapter2 TTCTTTCCCCCACCCTTTCC  --length 75 $SL  $SR  

SL=${STEM}_FV_L_val_1_val_1.fq
SR=${STEM}_FV_R_val_2_val_2.fq

mv $SL Val_${STEM}_L.fq
mv $SR Val_${STEM}_R.fq


rm *val_[12].fq

SL=Val_${STEM}_L.fq
SR=Val_${STEM}_R.fq

~/src_code/trim_galore_zip/trim_galore -a TGATGCTTTCGAACGTCT -a2 TTCGAACCAGGGGTACCG --paired --length 75 $SL  $SR
SL=Val_${STEM}_L_val_1.fq
SR=Val_${STEM}_R_val_2.fq
~/src_code/trim_galore_zip/trim_galore -a TCTACGG  -a2  ACCCGGGGTACCGAAT --paired --length 75 $SL  $SR
SL=Val_${STEM}_L_val_1_val_1.fq
SR=Val_${STEM}_R_val_2_val_2.fq
~/src_code/trim_galore_zip/trim_galore  -a AATACGGAGCTT -a2 AATACGGAGCTT --paired --length 75 $SL  $SR

SL=Val_${STEM}_L_val_1_val_1_val_1.fq
SR=Val_${STEM}_R_val_2_val_2_val_2.fq

mv $SR Val2_${STEM}_R.fq
mv $SL Val2_${STEM}_L.fq

for FILE in Val2_${STEM}_[LR].fq
		do 
			ln -s $FILE . 
			fastqc $FILE --outdir qc
			fastx_quality_stats -i $FILE -o qc/${FILE}.fastx_stats
		done




