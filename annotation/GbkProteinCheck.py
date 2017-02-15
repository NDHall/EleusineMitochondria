#!/usr/bin/python

#=============================================

#        This script is for double checking
#        the protein sequences in a genbank
#        file. It is for peace of mind and
#        to make sure that all sequences are
#        correctly  assembled and annontated.
#        We are looking at taking out each of
#        protein sequences and comparing them
#        to a standarized protein query using
#        biopython, paired with blast.
#=============================================

# required modules

from Bio import SeqIO
from Bio import SeqRecord
import argparse

#=============================================

#        Now lets make some functions

#=============================================


#        FeatureSeqExtract takes a genbank file
#        and returns all features sorted into
#        categories based on CDS,
#        tRNA, rRNA, and gene.

#=============================================


def FeatureSeqExtract(GBK):
    
                           
    counter=1
    ParsedFeatures={"CDS":[], "tRNA":[], "rRNA":[], "all":[]}
    record=SeqIO.read(GBK,"genbank")
    seq=str(record.seq)
    for feature in record.features:
        if feature.type == "CDS" and "translation" in feature.qualifiers:
            ParsedFeatures[feature.type].append([feature.qualifiers["gene"][0],feature.qualifiers["translation"][0]])
        elif ( feature.type == "tRNA" or
        feature.type == "rRNA" ):
            ParsedFeatures[feature.type].append([feature.qualifiers["gene"][0],seq[feature.location.start.position:feature.location.end.position]])
        else:
            if "gene"  in  feature.qualifiers:
                name=feature.qualifiers["gene"][0]
            elif "note" in feature.qualifiers:
                name=feature.qualifiers["note"][0]
            else:
                name="un-named_"+str(counter)
                counter+=1
            ParsedFeatures["all"].append([name,seq[feature.location.start.position:feature.location.end.position]])
    return ParsedFeatures


def PrintParsedFeatures(ParsedFeatures, StemHandle, MaxLen):
   
    for category in ParsedFeatures:
        OutString=""
        for entry in ParsedFeatures[category]:
            if len(entry[1]) > 0 and len(entry[1])< MaxLen:
                OutString+=">"+entry[0]+"\n"+entry[1]+"\n"
        f=open(StemHandle+"_"+category+".fasta",'w')
        f.write(OutString)
        f.close()
        del OutString

#=============================================

#        Now use of functions

#=============================================

parser=argparse.ArgumentParser()
parser.add_argument("GBK", help="Genbank file for feature extaction into 4 seprate files based on CDS, tRNA, rRNA, all categories which extracts genes, misc_features etc.. that are less than 8Kbp. This effectively excludes trans-spliced genes and large genes. Which should not be a problem for the plant mitochondrial genomes this was written for, but it will limit its application.")
parser.add_argument("StemHandle", help="Stem for output which will be Stem_(category).fasta. Script is written to write over existing files. So pick unique stem names or be aware that the files produced with an identical stem name will be overwritten.")
args=parser.parse_args()

GBK=FeatureSeqExtract(args.GBK)
PrintParsedFeatures(GBK, args.StemHandle,8000)





                                        
        
        
            
            
    
    
    



                                        


