# script to add Tax
#commented out the Tax labeling.

TOT=$1
FOLD=$2
 for X in $(sed 's/ /###/g' ${TOT}) ; do ID=$( echo $X | cut -d "#" -f 1);SP=$( grep $ID ../../Keys/SRA_GPWG_order.txt | awk '{print $2"_"$3}'); LIN=$( grep $ID ../../Keys/SRA_GPWG_order.txt | awk  '{print $4" Null Null "}' |  sed 's/;/ /g' ); echo $SP $ID; echo $X $LIN $SP| sed 's/###/ /g'>>${FOLD} ; done


#Series to add Null for fields

echo $( awk 'NF==9' ${FOLD}| sed 's/Null Null/Null Null Null Null Null Null/' | awk '{print NF}' | sort | uniq -c  )


awk 'NF==9' ${FOLD}| sed 's/Null Null/Null Null Null Null Null Null/'
awk 'NF==9' ${FOLD}| sed 's/Null Null/Null Null Null Null Null Null/' > tmp.table
awk 'NF==10' ${FOLD}| sed 's/Null Null/Null Null Null Null Null/' >> tmp.table
 awk 'NF==11' ${FOLD}| sed 's/Null Null/Null Null Null Null/' >> tmp.table
 awk 'NF==12' ${FOLD}| sed 's/Null Null/Null Null Null/' >> tmp.table
 awk 'NF==13' ${FOLD}| sed 's/Null Null/Null Null/' >> tmp.table
mv tmp.table ${FOLD} 
