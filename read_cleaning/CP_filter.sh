L=$1
R=$2
STEM=$3

	bowtie2 -x CP_Filt/El_CP_Draft_10 --rg-id ${STEM} --threads 15 -1 ${L} -2 ${R} -S ${STEM}_ALL.sam
        # make directory to keep raw reads clean
	mkdir $STEM
	mv ${STEM}_ALL.sam $STEM
	cd $STEM


	#samtools sequence to extract interleaved *.sam file from mapped reads

	samtools view -@ 4 -bS ${STEM}_ALL.sam |samtools sort -n - $STEM
	samtools view -H ${STEM}_ALL.sam >$STEM.header
	samtools index $STEM.bam
	samtools view  -@ 4 -h -f 8 -f 4 $STEM.bam > ${STEM}_unmap.sam


	samtools view -@ 4 -bS ${STEM}_unmap.sam | samtools sort -n - ${STEM}_unmap
	samtools index ${STEM}_unmap.bam
	samtools bam2fq -s ${STEM}_sflag.fq ${STEM}_unmap.bam > ${STEM}_unmap.fq
	sickle pe --qual-type sanger -c ${STEM}_unmap.fq  -m ${STEM}_len90q20.fq -s Sing_${STEM}_len90q20.fq -l 90 -q 20 
	fastq_chomp_split.py  ${STEM}_len90q20.fq   ${STEM}_len90q20
	rm *sam *bam* 



	cd ..	



	for FILE in ${STEM}/*[LR].fq
		do 
			ln -s $FILE . 
			fastqc $FILE --outdir qc
			fastx -i $FILE -o qc/${FILE}.fastx_stats
		done
					
 



