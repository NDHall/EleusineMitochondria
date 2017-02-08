L=$1
R=$2
STEM=$3

	bowtie2 -x  /home/biolinux/Eluisine/Mito/PipeLine/vectors/pPV576.fasta --rg-id ${STEM} --local  --threads 15 -1 ${L} -2 ${R} -S ${STEM}_ALL.sam
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
	fastq_chomp_split.py  ${STEM}_unmap.fq   ${STEM}_FV
	rm *sam *bam* 



	cd ..	



	for FILE in ${STEM}/*[LR].fq
		do 
			ln -s $FILE . 
			fastqc $FILE --outdir qc
			fastx -i $FILE > qc/${FILE}.fastx_stats
		done
					
 



