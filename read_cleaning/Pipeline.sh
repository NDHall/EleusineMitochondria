#!/bin/bash

# begining to end pipeline to be used for Eleusine mitochondrial read cleaning and assembly

# Raw Variables

#RUN augenomics [1] 1709


RD_L=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_L.fastq#RD_L
RD_R=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_R.fastq#RD_R
MP_L=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1-7k/SM01-PBU1-7k_CCGTCC_L005_R1_001.fastq#MP_L
MP_R=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1-7k/SM01-PBU1-7k_CCGTCC_L005_R2_001.fastq#MP_R
PE_L=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1/SM01-PBU1_GTCCGC_L005_R1_001.fastq#PE_L
PE_R=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1/SM01-PBU1_GTCCGC_L005_R2_001.fastq#PE_R

# Stems will be called on fly.

#begin with intial quality scores from fastqc
#P short for Path
#S short for STEM

# IntitialQC

#mkdir qc
#for X in  $RD_L $RD_R $MP_L $MP_R $PE_L $PE_R
#	do 
	# here unpack STEM and PATH from variable.
#	 P=$(echo $X | cut -d'#' -f -1 )
#	 S=$(echo $X | cut -d'#' -f 2- )
		

#	echo "
#		working on  $S $P
#"#

#fastqc $P --outdir qc

	

#done


#Trimming stages


# On campus READS
# majority of problem seems to be in in the firs 12 bases. So we will trim these. Then look for an eliminate regular illumia reads.
# over represented kmers also include CP and ITS reads as well as possible pentacopetide repeats. So being careful here is a plus. By elminating the first 12-15 there should
# be plenty left over to still use. 


#DNA reads from on campus 


L=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_L.fastq
R=/home/biolinux/Eluisine/CP/raw_data/Sample_DNA-1/DNA_1_R.fastq

STEM=RD


 ./CP_filter.sh $L $R $STEM >>output.txt

SL=${STEM}_len90q20_L.fq
SR=${STEM}_len90q20_R.fq


~/src_code/trim_galore_zip/trim_galore --paired --illumina --length 90 --clip_R2 15 --length 75 $SL  $SR  >>output.txt

SL=${STEM}_len90q20_L_val_1.fq
SR=${STEM}_len90q20_R_val_2.fq


~/src_code/trim_galore_zip/trim_galore --paired --adapter2 TTCTTTCCCCCACCCTTTCC  --length 75 $SL  $SR  

SL=${STEM}_len90q20_L_val_1_val_1.fq
SR=${STEM}_len90q20_R_val_2_val_2.fq

mv $SL Val_${STEM}_L.fq
mv $SR Val_${STEM}_R.fq

for FILE in Val_${STEM}_[LR].fq
		do 
			ln -s $FILE . 
			fastqc $FILE --outdir qc
			fastx_quality_stats -i $FILE -o qc/${FILE}.fastx_stats
		done


rm *val_[12].fq


#	Mate pair


L=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1-7k/SM01-PBU1-7k_CCGTCC_L005_R1_001.fastq
R=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1-7k/SM01-PBU1-7k_CCGTCC_L005_R2_001.fastq
STEM=MP


# CP filter

./CP_filter.sh $L $R $STEM

SL=${STEM}_len90q20_L.fq
SR=${STEM}_len90q20_R.fq


~/src_code/trim_galore_zip/trim_galore --paired --nextera $SL  $SR 2>>output.txt

SL=${STEM}_len90q20_L_val_1.fq
SR=${STEM}_len90q20_R_val_2.fq

~/src_code/trim_galore_zip/trim_galore --paired --illumina $SL  $SR  >>output.txt
SL=${STEM}_len90q20_L_val_1_val_1.fq
SR=${STEM}_len90q20_R_val_2_val_2.fq

~/src_code/trim_galore_zip/trim_galore -a GTCTCTTATACACATCTAGATGTGTATAAGAGACAG -a2 GTCTCTTATACACATCTAGATGTGTATAAGAGACAG --paired --length 90 $SL  $SR

SL=${STEM}_len90q20_L_val_1_val_1_val_1.fq
SR=${STEM}_len90q20_R_val_2_val_2_val_2.fq


mv $SL Val_${STEM}_L.fq
mv $SR Val_${STEM}_R.fq

for FILE in Val_${STEM}_[LR].fq
		do 
			ln -s $FILE . 
			fastqc $FILE --outdir qc
			fastx_quality_stats -i $FILE -o qc/${FILE}.fastx_stats
		done

rm *val_[12].fq


L=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1/SM01-PBU1_GTCCGC_L005_R1_001.fastq
R=/home/biolinux/Eluisine/CP/raw_data/Sample_SM01-PBU1/SM01-PBU1_GTCCGC_L005_R2_001.fastq
STEM=PE


# PE Filter

./CP_filter.sh $L $R $STEM >>output.txt

SL=${STEM}_len90q20_L.fq
SR=${STEM}_len90q20_R.fq


~/src_code/trim_galore_zip/trim_galore --paired --illumina --length 90 $SL  $SR  >>output.txt

SL=${STEM}_len90q20_L_val_1.fq
SR=${STEM}_len90q20_R_val_2.fq


mv $SL Val_${STEM}_L.fq
mv $SR Val_${STEM}_R.fq

for FILE in Val_${STEM}_[LR].fq
		do 
			ln -s $FILE . 
			fastqc $FILE --outdir qc
			fastx_quality_stats-i $FILE -o qc/${FILE}.fastx_stats
		done

rm *val_[12].fq

		





