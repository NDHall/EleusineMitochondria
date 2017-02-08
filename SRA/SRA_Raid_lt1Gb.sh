#!/bin/bash

LIST=$1

COUNTER=1
for X in $(cat $LIST)
do 
	STUB=$(echo $X |cut -b -3 ) 
	STEM=$(echo $X |cut -b -6) 
	echo Working on $STEM $X 
	echo wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/${STUB}/${STEM}/${X}/${X}.sra 
	wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/${STUB}/${STEM}/${X}/${X}.sra
	
	let COUNTER=COUNTER+1
	if [ $(( COUNTER % 4 )) -eq 0 ] ;
	then
	echo "	

		I'm just going to chill for a bit

"

 	
		sleep 1500
	fi




done
