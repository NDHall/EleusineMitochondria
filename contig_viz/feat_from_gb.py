#!/usr/bin/python

# Script to extract selected features
###########################################################################################################
#required packages


import argparse
from Bio import SeqIO


#IMPORT ARGS FROM CLE#
#############################################################################################################



parser=argparse.ArgumentParser()
parser.add_argument("GB_HANDLE", help="Required Genbank file")

args=parser.parse_args()

# STEM Creation

GB=args.GB_HANDLE
STEM_gb=(GB.split("/"))[-1] # this command take last partion of file path. Thus this script will always output to current directory.
STEM=STEM_gb.replace(".gb","") # to create true stem remove final .gb



print "\n\n\t"+STEM+"\t"+ GB+"\n\n"

# Parsing File
# taken with minimal modification https://github.com/peterjc/biopython_workshop/blob/master/using_seqfeatures/README.rst
record=SeqIO.read(GB,"genbank")
output_handle=open((STEM+".fasta"),"w")
count=0

Extract_list=["tRNA","CDS","rRNA"]

for feature in record.features:
	if feature.type in Extract_list:
		#print feature.type
		#print (feature)
		count+=1
		if "product" in feature.qualifiers and "gene" in feature.qualifiers and "product" in feature.qualifiers:
			feature_name=(STEM+":"+((str(feature.qualifiers["gene"])+":"+str(feature.qualifiers["product"])).replace("[","")).replace("]","").replace("'","")) # this long nasty command is just removing unwanted characters without writing a new variable. Not the best but it could be much worse.
		else:
			feature_name=STEM+"MITO_FEAT"
		#print feature_name,"feature_name"
		feature_seq=feature.extract(record.seq)
		output_handle.write(">" + feature_name + "\n" + str(feature_seq) + "\n")

output_handle.close()

print(str(count) + " CDS sequences extracted"+STEM)


