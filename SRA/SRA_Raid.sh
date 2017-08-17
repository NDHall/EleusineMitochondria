#!/bin/bash


#List variable is a simple list of SRR accessions.
# USage SRA_Raid.sh [FILE_NAME]
# Sleep is optional likely. 


LIST=$1


for X in $(cat $LIST)
do 
	STUB=$(echo $X |cut -b -3 ) 
	STEM=$(echo $X |cut -b -6) 
	echo Working on $STEM $X 
	echo wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/${STUB}/${STEM}/${X}/${X}.sra 
	wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/${STUB}/${STEM}/${X}/${X}.sra
	
	echo " 

	Just finshed $X

"




done
