#!/bin/bash 

# script to run SRA mappings of insilico southern technique

 # filter here is 149 poales  chloroplast sequences. This should help cut down on cp contamination that seems to crop up here and there. 
FILTER=/home/biolinux/Eluisine/SRA/SRA_Ana/3rdGen/PoaCpSeq.fasta

SOUTHERN=$1
SouStem=$( echo $SOUTHERN |rev| cut -d"/" -f -1| cut -d"." -f 2|rev )
echo $SouStem

##block for unpaired fastqs. 
### Check manually to add uncomment or not. If uncommented and no singletons. Leaves ugly files.

TEST=$(ls *[0-9][0-9].fastq | wc -w)


if [ $TEST -gt 0 ] ; then 

	for X in  *[0-9][0-9].fastq ;

		do 
		ReStem=$(  echo $X | sed 's/.fastq//' )
	#	head $L $R 
		echo "

	 
		Working on ${SouStem}_${ReStem}

	"
	# Block to filter out chloroplast reads.

#	FILT_SEQ=$( echo NoCP_${X} ) # 
#	STEM=$( echo CP_${X} |sed 's/.fastq//' ) 

#		bowtie2 -x  ${FILTER}   --threads 20 -U ${X} -S ${STEM}_ALL.sam


		#Old code block  This is too slow. It is easier to create a combined reference fasta with bad sequences labeled for exclusions.
		#The time this whole step was addding was painful especially for the large genome sequencing files.
		#It worked fine in theory on the genome skimming files.
		#So I am using a simpler alternative>
		#All cp genomic sequences will be labled with EXCLUDE in the reference>
		# a simple grep -v EXCLUDE should filter out all these sequences with out adding too much additional time.

	   
    # #samtools sequence to extract interleaved *.sam file from mapped reads

    # 	samtools view -bS ${STEM}_ALL.sam |samtools sort -n - $STEM
    # 	samtools view -H ${STEM}_ALL.sam >$STEM.header
    # 	samtools index $STEM.bam 
    #   	samtools view -h -f 4 $STEM.bam > ${STEM}_unmap.sam
	
    #   	rm  ${STEM}_ALL.sam $STEM.header  $STEM.bam 
    	
    # 	samtools view -bS ${STEM}_unmap.sam | samtools sort -n - ${STEM}_unmap
    
    # 	samtools bam2fq -s ${FILT_SEQ} ${STEM}_unmap.bam 




    # 	# This block is used to create Consensus reference from SRA 


		bowtie2 -x $SOUTHERN --threads 20 --local --no-unal -U $X  -S ${ReStem}_REF.sam
		samtools view -h ${ReStem}_REF.sam | egrep -v '[[:space:]]EXCLUDE'|samtools view -b -h  - >tmp.bam
		printf "\n\n\t\t Made tmp.bam\n\n"
		
		samtools sort tmp.bam  ${ReStem}_REF
	        samtools index ${ReStem}_REF.bam
		samtools mpileup -v -f $SOUTHERN  ${ReStem}_REF.bam| bcftools call -c -O z >${ReStem}_REF.vcf.gz
		tabix ${ReStem}_REF.vcf.gz 
		bcftools consensus -f $SOUTHERN ${ReStem}_REF.vcf.gz > ${ReStem}_REF_${SouStem}.fa

	##record some basic numbers about preliminary mapping

		samtools idxstats ${ReStem}_REF.bam | awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  > ${ReStem}_REF.stats
		samtools depth ${ReStem}_REF.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}'> ${ReStem}_REF.depth
		samtools view -H ${ReStem}_REF.bam >>REF.log
		TotalDepth_Normalizer_InSiSouth_forControl.py ${ReStem}_REF.stats ${ReStem}_REF.depth ${ReStem}_REF.stats ${ReStem}_REF.depth
		rm REF.sam  #.bam REF.vcf.gz* REF.bam.bai


	##BLOCK USED TO CREATE STATS

		bowtie2-build -q ${ReStem}_REF_${SouStem}.fa ${ReStem}_REF_${SouStem}.fa
		nice -n 5 bowtie2 -x ${ReStem}_REF_${SouStem}.fa  --threads 20  --local --no-unal -U $X -S ${SouStem}_${ReStem}.sam
		samtools view -h  ${SouStem}_${ReStem}.sam| egrep -v '[[:space:]]EXCLUDE' | samtools view -b -h  - | samtools sort - ${SouStem}_${ReStem}
		samtools index ${SouStem}_${ReStem}.bam
		samtools depth ${SouStem}_${ReStem}.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}' >>${SouStem}_${ReStem}_TotalDepth.table
		samtools idxstats ${SouStem}_${ReStem}.bam |  awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  >>${SouStem}_${ReStem}_idxstats.table
		rm ${SouStem}_${ReStem}.sam
		TotalDepth_Normalizer_InSiSouth_forControl.py ${SouStem}_${ReStem}_idxstats.table ${SouStem}_${ReStem}_TotalDepth.table ${SouStem}_${ReStem}_idxstats.table ${SouStem}_${ReStem}_TotalDepth.table

	rm   *${ReSTEM}*bt2  *${ReSTEM}*tbi *${ReSTEM}*sam *${ReSTEM}*gz

	done 
fi

TEST2=$(ls *_1.fastq | wc -w)


	if [ $TEST2 -gt 0 ] ; then 
	for L in *_1.fastq 
		do R=$( echo $L | sed 's/_1.fastq/_2.fastq/' )
		ReStem=$(  echo $L | sed 's/_1.fastq//' )
	#	head $L $R 
		echo "

	 
		Working on ${SouStem}_${ReStem}

	"


#This whole section has been commented out so that we can use a simpler approach outlined above.

		# 	# Price Filter block discards reads that have big hits to chloroplast at the nucleotide level

    # 	L_SEQ=$( echo NoCP_${L} )

		
    # 		# Block to filter out chloroplast reads.


    # 	STEM=$( echo CP_${X} |sed 's/.fastq//' )

    # 		bowtie2 -x   ${FILTER} --threads 20 -1 $L -2 $R  -S ${ReStem}_ALL.sam



    # #samtools sequence to extract interleaved *.sam file from mapped reads

    # 	samtools view -bS -@ 10 ${ReStem}_ALL.sam |samtools sort -@ 10 -n - $STEM
    # 	samtools view -H ${STEM}_ALL.sam >$STEM.header
    # 	samtools index $STEM.bam 
    #   	samtools view -@ 10 -h -f 8 -f 4 $STEM.bam > ${STEM}_unmap.sam
	
    #   	rm  ${STEM}_ALL.sam $STEM.header  $STEM.bam 
    	
    # 	samtools view -@ 10 -bS ${STEM}_unmap.sam | samtools sort -@ 10 -n - ${STEM}_unmap
    # 	samtools bam2fq -s OUT.$STEM ${STEM}_unmap.bam > $L_SEQ


    # 	fastq_chomp_split.py $L_SEQ NoCP_${ReStem} #_[RL].fq is appended to STEM given to fastq_chomp_split.py
    # 	rm $L_SEQ OUT.$STEM



	
	# This block is used to create Consensus reference from SRA 


		bowtie2 -x $SOUTHERN --threads 20 --local --no-unal -1 $L -2 $R -S ${ReStem}_REF.sam
		samtools view  -h ${ReStem}_REF.sam| egrep -v '[[:space:]]EXCLUDE'| samtools view -b -h - >tmp.bam
		echo Made tmp.bam
		samtools sort  tmp.bam  ${ReStem}_REF
		samtools index ${ReStem}_REF.bam
		samtools mpileup -v -f $SOUTHERN  ${ReStem}_REF.bam| bcftools call -c -O z >${ReStem}_REF.vcf.gz
		tabix ${ReStem}_REF.vcf.gz 
		bcftools consensus -f $SOUTHERN ${ReStem}_REF.vcf.gz > ${ReStem}_REF_${SouStem}.fa

	##record some basic numbers about preliminary mapping

		samtools idxstats ${ReStem}_REF.bam | awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  > ${ReStem}_REF.stats
		samtools depth ${ReStem}_REF.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}'> ${ReStem}_REF.depth
		samtools view -H ${ReStem}_REF.bam >>REF.log
	#	TotalDepth_Normalizer_InSiSouth_forControl.py ${ReStem}_REF.stats ${ReStem}_REF.depth ${ReStem}_REF.stats ${ReStem}_REF.depth
	#Block to aggregate all numbers
	 	samtools depth ${SouStem}_${ReStem}.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}' >> Total_${ReStem}_TotalDepth.table
		samtools idxstats ${SouStem}_${ReStem}.bam |  awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  >> Total_${ReStem}_idxstats.table
		TotalDepth_Normalizer_InSiSouth_forControl.py Total_${ReStem}_idxstats.table Total_${ReStem}_TotalDepth.table Total_${ReStem}_idxstats.table Total_${ReStem}_TotalDepth.table
	

	#BLOCK USED TO CREATE STATS

		bowtie2-build -q ${ReStem}_REF_${SouStem}.fa ${ReStem}_REF_${SouStem}.fa
		nice -n 5 bowtie2 -x ${ReStem}_REF_${SouStem}.fa  --threads 20  --local --no-unal -1 $L -2 $R -S ${SouStem}_${ReStem}.sam
		samtools view -h ${SouStem}_${ReStem}.sam| egrep -v '[[:space:]]EXCLUDE'| samtools view -b -h  -  | samtools sort -@ 10 - ${SouStem}_${ReStem}
		samtools index ${SouStem}_${ReStem}.bam
		samtools depth  ${SouStem}_${ReStem}.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}' >${SouStem}_${ReStem}_TotalDepth.table
		samtools idxstats ${SouStem}_${ReStem}.bam |  awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  >${SouStem}_${ReStem}_idxstats.table
		rm ${SouStem}_${ReStem}.sam
		
		samtools depth ${SouStem}_${ReStem}.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}' >>Total_${ReStem}_TotalDepth.table
		samtools idxstats ${SouStem}_${ReStem}.bam |  awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  >>Total_${ReStem}_idxstats.table
		TotalDepth_Normalizer_InSiSouth_forControl.py Total_${ReStem}_idxstats.table Total_${ReStem}_TotalDepth.table Total_${ReStem}_idxstats.table Total_${ReStem}_TotalDepth.table

		
	rm  *${ReSTEM}*bt2  *${ReSTEM}*tbi *${ReSTEM}*sam *${ReSTEM}*gz

	done 
fi 




