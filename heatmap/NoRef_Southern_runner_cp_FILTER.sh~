#!/bin/bash 
GIT_REPO=/home/biolinux/Eluisine/EleusineMitochondria_scripts/heatmap
PATH=${GIT_REPO}:${PATH}


# script to run SRA mappings of insilico southern technique
# Some General Notes
#     Filtering with egrep 
		# egrep command below is used to exclude unwanted to reads, to accomplish this I have created a reference file which contains
		# both sequences to filter out and keep. This provides 2 advantages, it reduces the time it would take to create a filtered
		# set of reads using bowtie2 and samtools  and it put sequences in situation where they are competitively mapped. 
		# With competitve mapping the reads must be assigned to the best fit sequence which should be the filtering one.
		# using egrep for the whole line elimnates all read pairs for which 1 of the reads maps to a filter sequence 
#    TotalDepth_Normalizer_InSiSouth_forControl.py *_idxstats.table *TotalDepth.table *_idxstats.table *_TotalDepth.table
#                 This rather larger script takes in modified depth and idx tables from samtools see awk commands below.
#                 It was orginally designed to take in a normalizing idxstats.table and depth.table along
#                 with a variable idxstats.table and depth.table
#                 Here I am combining all measurements into 1 output file and running it through script that way.
#                 This is not short term a problem because the normalizing  gene names are hard coded into the python script.
#                 Long term the script needs to be updated, or used as it was orginally intended with normalizing gene names
#                 no longer hard coded into the script.
#                 Short term solution is to tag Control genes and put them into their own table and then use this to run script as
#                 intended. When doing multiple runs like with introns vs exons. The exons with the control group must be put first or
#                 There will be no control sequence.
#                 Also note, these analyses should be done in clean directory or the Control tables can and will become contaminated this is
#                 because I am using the append function.







SOUTHERN=$1 # Name of reference fasta file that is identical to the bowtie2 index name.

SouStem=$( echo $SOUTHERN |rev| cut -d"/" -f -1| cut -d"." -f 2|rev )

#     block for unpaired fastqs. 
##          This is lieu of checking manually. SRA-split-3 fuction creates predictable fastq names which we are using here.
##          If we want to modify this for other fastq files this would be a place to watch


TEST=$(ls *[0-9][0-9].fastq | wc -w)


if [ $TEST -gt 0 ] ; then 

	for X in  *[0-9][0-9].fastq ;

		do 
		ReStem=$(  echo $X | sed 's/.fastq//' )
 
		printf "\n\n\tWorking on ${SouStem}_${ReStem}\n\n"
		
		bowtie2 -x $SOUTHERN --threads 20 --local --no-unal -U $X  -S ${ReStem}_REF.sam


		samtools view -h ${ReStem}_REF.sam | egrep -v '[[:space:]]EXCLUDE'|samtools view -b -h  - >tmp.bam
		printf "\n\n\t\t Made tmp.bam\n\n"
		
		samtools sort tmp.bam  ${ReStem}_REF
	        samtools index ${ReStem}_REF.bam
		samtools mpileup -v -f $SOUTHERN  ${ReStem}_REF.bam| bcftools call -c -O z >${ReStem}_REF.vcf.gz
		tabix ${ReStem}_REF.vcf.gz 
		bcftools consensus -f $SOUTHERN ${ReStem}_REF.vcf.gz > ${ReStem}_REF_${SouStem}.fa

	##record some basic numbers about preliminary mapping

		samtools idxstats ${ReStem}_REF.bam | awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  > ${ReStem}_REF_${SouStem}.stats
		samtools depth ${ReStem}_REF.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}'> ${ReStem}_REF_${SouStem}.depth
		samtools view -H ${ReStem}_REF.bam >>REF.log
		rm tmp.bam *REF.sam  *REF.bam* *REF.vcf.gz* 


	##BLOCK USED TO CREATE STATS

		bowtie2-build -q ${ReStem}_REF_${SouStem}.fa ${ReStem}_REF_${SouStem}.fa
		nice -n 5 bowtie2 -x ${ReStem}_REF_${SouStem}.fa  --threads 20  --local --no-unal -U $X -S ${SouStem}_${ReStem}.sam
		samtools view -h  ${SouStem}_${ReStem}.sam| egrep -v '[[:space:]]EXCLUDE' | samtools view -b -h  - | samtools sort - ${SouStem}_${ReStem}
		samtools index ${SouStem}_${ReStem}.bam
		samtools depth ${SouStem}_${ReStem}.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}' >>${SouStem}_${ReStem}_TotalDepth.table
		samtools idxstats ${SouStem}_${ReStem}.bam |  awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  >>${SouStem}_${ReStem}_idxstats.table
		rm ${SouStem}_${ReStem}.sam *REF.bam*
		
		# Normalizer sequences should be embedded in mapping file where appropriate.
		# In this case they must be named with unique word control.
		# Filter sequences must be tagged with the unique label EXCLUDE.
		# If this script is run iteratively in a larger pipeline
		# the reference files which contain the control sequences must be processed first
		# or there will be nothing to normalizer the other sequences with.

		
		grep Control ${SouStem}_${ReStem}_idxstats.table >> Normalizer_${ReStem}_idxstats.table
		grep -v EXCLUDE ${SouStem}_${ReStem}_idxstats.table >> All_${ReStem}_idxstats.table
		grep Control  ${SouStem}_${ReStem}_TotalDepth.table >> Normalizer_${ReStem}_TotalDepth.table
		grep -v EXCLUDE  ${SouStem}_${ReStem}_TotalDepth.table >> All_${ReStem}_TotalDepth.table
		rm  ${SouStem}_${ReStem}_TotalDepth.table  ${SouStem}_${ReStem}_idxstats.table
		TotalDepth_Normalizer_InSiSouth_forControl.py Normalizer_${ReStem}_idxstats.table Normalizer_${ReStem}_TotalDepth.table All_${ReStem}_idxstats.table All_${ReStem}_TotalDepth.table

	rm   tmp.bam *${ReSTEM}*bt2  *${ReSTEM}*tbi *${ReSTEM}*sam *${ReSTEM}*gz

	done 
fi

TEST2=$(ls *_1.fastq | wc -w)


	if [ $TEST2 -gt 0 ] ; then 
	for L in *_1.fastq 
		do R=$( echo $L | sed 's/_1.fastq/_2.fastq/' )
		ReStem=$(  echo $L | sed 's/_1.fastq//' )
	#	head $L $R 
		printf "\n\n\t\tWorking on ${SouStem}_${ReStem}\n\n"
	# This block is used to create Consensus reference from SRA 
         	bowtie2 -x $SOUTHERN --threads 20 --local --no-unal -1 $L -2 $R -S ${ReStem}_REF.sam
		samtools view  -h ${ReStem}_REF.sam| egrep -v '[[:space:]]EXCLUDE'| samtools view -b -h - >tmp.bam
		samtools sort  tmp.bam  ${ReStem}_REF
		samtools index ${ReStem}_REF.bam
		samtools mpileup -v -f $SOUTHERN  ${ReStem}_REF.bam| bcftools call -c -O z >${ReStem}_REF.vcf.gz
		tabix ${ReStem}_REF.vcf.gz 
		bcftools consensus -f $SOUTHERN ${ReStem}_REF.vcf.gz > ${ReStem}_REF_${SouStem}.fa

	##record some basic numbers about preliminary mapping

		samtools idxstats ${ReStem}_REF.bam | awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  > ${ReStem}_REF_${SouStem}.stats
		samtools depth ${ReStem}_REF.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}'> ${ReStem}_REF_${SouStem}.depth
		samtools view -H ${ReStem}_REF.bam >>REF.log

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

		samtools view -h  ${SouStem}_${ReStem}.sam| egrep -v '[[:space:]]EXCLUDE' | samtools view -b -h  - | samtools sort - ${SouStem}_${ReStem}
		samtools index ${SouStem}_${ReStem}.bam
		samtools depth ${SouStem}_${ReStem}.bam | awk -v ReStem=$ReStem '{print ReStem,$1,$2,$3}' >>${SouStem}_${ReStem}_TotalDepth.table
		samtools idxstats ${SouStem}_${ReStem}.bam |  awk  '{print ReSTEM,$1, $2,$3,$4 }' ReSTEM=$ReStem  >>${SouStem}_${ReStem}_idxstats.table
		rm ${SouStem}_${ReStem}.sam
		
		# Normalizer sequences should be embedded in mapping file where appropriate.
		# In this case they must be named with unique word control.
		# Filter sequences must be tagged with the unique label EXCLUDE.
		# If this script is run iteratively in a larger pipeline
		# the reference files which contain the control sequences must be processed first
		# or there will be nothing to normalizer the other sequences with.

		
		grep Control ${SouStem}_${ReStem}_idxstats.table >> Normalizer_${ReStem}_idxstats.table
		grep -v EXCLUDE ${SouStem}_${ReStem}_idxstats.table >> All_${ReStem}_idxstats.table
		grep Control  ${SouStem}_${ReStem}_TotalDepth.table >> Normalizer_${ReStem}_TotalDepth.table
		grep -v EXCLUDE  ${SouStem}_${ReStem}_TotalDepth.table >> All_${ReStem}_TotalDepth.table
		rm  ${SouStem}_${ReStem}_TotalDepth.table  ${SouStem}_${ReStem}_idxstats.table

		
		TotalDepth_Normalizer_InSiSouth_forControl.py Normalizer_${ReStem}_idxstats.table Normalizer_${ReStem}_TotalDepth.table All_${ReStem}_idxstats.table All_${ReStem}_TotalDepth.table

		
	rm  *${ReSTEM}*bt2  *${ReSTEM}*tbi *${ReSTEM}*sam *${ReSTEM}*gz

	done 
fi 




