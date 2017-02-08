#!/bin/bash
# scripts used to cosolidate all fastas
#script used to create series of alignments for MT genes
#for X in *.fasta ; do echo $X | cut -d"_" -f -2 ; done | sort |uniq > AccList.txt
#for X in $( ls | egrep -v 'Final_|nohup') ;do mv $X RawFastas/ ;done
#cp  ../SRA_Ana/Refs/1stGeneration/Refined_Zea_II.fasta  Zea_Exons.fasta
#ndh0004@venus:/home/biolinux/Eluisine/SRA/SRA_Assems/exons$ for X in ../Consensus/Final_*.fasta ;do ../NDH_Blast_to_Align.sh Zea_Exons.fasta $X ; done

DB=$1		
Q_DIR=$2 #directory containg only fasta  files 

for Q in ${Q_DIR}/*fasta ; do 

	/automnt/opt/ncbi-blast/2.4.0/bin/blastn -query $Q -db $DB  -max_target_seqs 1 -max_hsps 1 -outfmt '6 slen length qseqid sseqid qseq score'| sed '/>/! s/-//g' >>Blastn.out

done 

#for Preliminary_Sorting.
	awk '{print $4}' Blastn.out | sort | uniq  >Gene.list
	awk '{print $3}' Blastn.out | sort | uniq  >Acc.list

 BestHitFasta.py Acc.list Gene.list Blastn.out

for X in *fa; do

	/automnt/opt/mafft/default/bin/mafft   --auto --clustalout --inputorder $X > aln_${X}

	done

