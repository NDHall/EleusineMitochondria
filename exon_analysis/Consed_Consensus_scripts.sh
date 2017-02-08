#!/bin/bash

#begin by setting up folders we will do this manually but I am putting commands here for future ref.
# mkdir BOP && cd BOP
#ndh0004@venus:/home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/BOP$ for X in $( grep BOP /home/biolinux/Eluisine/SRA/SRA_Ana/Keys/Mod_SRA_taxonomy_key.txt |cut -d"#" -f -1 ); do for Y in /home/biolinux/Eluisine/SRA/fqs/${X}* ; do echo $Y ;ln -s $Y . ; done ; done
# cd ../ && mkdir PACMAD && cd PACMAD
#ndh0004@venus:/home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active$ for X in *fasta ;do bowtie2-build $X $X -q ; done 

# Move into folder for Rice REF this one is smaller and we should be able to detect trouble faster. 


cd BOP
 

# Structure of command = Consenus_from_Rawfq.sh [ Reference FASTA ]

#~/scripts/bash/Consenus_from_Rawfq.sh /home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/Refined_OrySat_IV.fasta
#~/scripts/bash/Consenus_from_Rawfq.sh /home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/iOryVI.fasta
~/scripts/bash/Consenus_from_Rawfq.sh /home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/EleusineOrfs.fasta
cd /home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/PACMAD


# Now doing same for PACMAD clade. This will matter most with regard to introns. 
# 
#~/scripts/bash/Consenus_from_Rawfq.sh /home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/Refined_Zea_IV.fasta
#~/scripts/bash/Consenus_from_Rawfq.sh /home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/iZeaIV.fasta
~/scripts/bash/Consenus_from_Rawfq.sh /home/biolinux/Eluisine/SRA/SRA_Assems/Ref3/Active/EleusineOrfs.fasta






