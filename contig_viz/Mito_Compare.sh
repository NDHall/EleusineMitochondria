#!/bin/bash

REF=$1
CONTIG=$4
CP=$2
REPEATS=$3

# Script to take a ref genome *.gb file  and set of contigs to create 
# blast db
# Custom blast result to be parsed by python scripts
# Primitive .gffe
# Basic Bed file
# illustrations of gene hits including trna, CDS, ribosomal subunits
#	Please note tRNA are only provisional and need to be verifed by cove or some related software


STEM=$( echo $CONTIG|rev|cut -d'/' -f -1|cut -d'.' -f 2- |rev)
Use_REF=$( echo $REF|rev|cut -d'/' -f -1|rev)
Use_CONTIG=$( echo $CONTIG|rev|cut -d'/' -f -1|rev)
Use_CP=$( echo $CP|rev|cut -d'/' -f -1|rev)
Use_REP=$(  echo $REPEATS |rev|cut -d'/' -f -1|rev)
if [ -d $STEM ] 
	then 
		echo "


		DIR $STEM Exists please create new folder for analysis


"
		exit
else
	echo "
		Making DIR $STEM

"
	mkdir $STEM

fi
# move files into normal folder
	cp $REF ${STEM}/${Use_REF}
	cp $CONTIG ${STEM}/${Use_CONTIG}
	cp $REPEATS ${STEM}/${Use_REP}
	cp $CP ${STEM}/${Use_CP}
cd $STEM


echo $(ls -thor) 
echo $( pwd )

feat_from_gb.py $Use_REF
Use_Ref_fasta=$( echo $Use_REF| rev | sed 's/bg./atsaf./'|rev )
echo "

		 $Use_Ref_fasta $Use_CP $Use_REP
"

makeblastdb -dbtype nucl -input_type fasta -in $Use_Ref_fasta -out $Use_Ref_fasta
makeblastdb -dbtype nucl -input_type fasta -in $Use_CP -out $Use_CP
makeblastdb -dbtype nucl -input_type fasta -in $Use_REP -out $Use_REP
blastn -query $Use_CONTIG  -db $Use_Ref_fasta -outfmt '6 qseqid sseqid qstart qend qlen  slen' -out ${STEM}.blastn_out
blastn -query $Use_CONTIG -db $Use_CP -outfmt '6 qseqid sseqid qstart qend qlen  slen' -out cp_${STEM}.blastn_out
blastn -query $Use_CONTIG -db $Use_REP -outfmt '6 qseqid sseqid qstart qend qlen  slen' -out self_${STEM}.blastn_out
grep -v 'orf' ${STEM}.blastn_out >PROT_${STEM}.blastn_out

mkdir ${STEM}_svgs

#-------------------------------------------------------------------------------------------------------

#		Below is the block of python functions I have written to parse the above blast into 
#		  different formats

#--------------------------------------------------------------------------------------------------------

blast_to_svg.py $STEM.blastn_out > ${STEM}_svgs/RAW_${STEM}.svg #creates raw svgs
# Don't need this right now # blast_to_svg_Custom.py $STEM.blastn_out ${STEM}_svgs/$STEM #creates svgs of genes specified in script 
blast_to_bed.py $STEM.blastn_out > $STEM.bed #creates bed file of blastn hits 
blast_to_gff3_prim.py $STEM.blastn_out #creates a gff3 file of blastn hits
blast_to_svg_Customv2.py  cp_${STEM}.blastn_out CP_${STEM} #CP insertions in green
blast_to_svg_RepeatSpecial.py self_${STEM}.blastn_out >Raw_${STEM}.svg # Repeat regions previously named. still a little cludgy
blast_to_svg_Customv2.py  PROT_${STEM}.blastn_out PROT_${STEM}



#-------------------------------------------------------------------------------------------------------


echo "




		 Finished working with $STEM



"
