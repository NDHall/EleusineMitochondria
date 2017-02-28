#!/usr/bin/python
import re
import argparse



#	house keeping


def clean_for_append(out):
	f=open(out,'w')
	f.write("")
	f.close()

#----------------------------------------------------------------------------------------------------------------
#	XARGS parser

parser=argparse.ArgumentParser()
parser.add_argument("HANDLE0", help="Input sam file goes here, ")

args=parser.parse_args()
HANDLE=args.HANDLE0



#--------------------------------------------------------------------------------------------------------------------------------------------

#		stem series now makes stem so that it out puts in the directory in which the command is given.

#-------------------------------------------------------------------------------------------------------------------------------------------

def STEM_MAKER(HANDLE,SUFFIX):
	stem=HANDLE.split(".")

	stem=".".join(stem[:-1])+SUFFIX
	stem=stem.split("/")
	stem=stem[-1]
	return stem



def STEM_MAKER(HANDLE,SUFFIX):
	stem=HANDLE.split(".")

	stem=".".join(stem[:-1])+SUFFIX
	stem=stem.split("/")
	stem=stem[-1]
	return stem

class blast_line:
	def __init__(self, qseqid, sseqid, qstart, qend, qlen, slen):
		self.qseqid=qseqid
		self.sseqid=sseqid
		self.qstart=qstart
		self.qend=qend
		self.qlen=qlen
		self.slen=slen

f=open(HANDLE,"r")
#Currently not using a write to file option just sending all to stout
stem=STEM_MAKER(HANDLE,".gff")
#out=open(stem,"a")


HEADER="##gff-version 3\n"
BODY=""
Chrom=""
counter=0


for Line in f:
	SLine=Line.split()

	if SLine>=7:
		BL=blast_line(SLine[0],SLine[1],SLine[2],SLine[3],SLine[4],SLine[5])
	else:
		break
	if Chrom !=BL.qseqid:
		OH=HEADER
		del HEADER
		HEADER=OH+"##sequence-region\t%s %s %s\n" %(BL.qseqid, "1", BL.qlen) 
		del OH
		OB=BODY
		del BODY
		BODY=OB+"###\n" 
		del OB
		Chrom=BL.qseqid
	if BL.qstart < BL.qend:
		OB=BODY
		del BODY
		BODY=OB+BL.qseqid+"\tblastn\tgene\t"+BL.qstart+"\t"+BL.qend+"\t.\t+\t.\t"+"ID="+BL.sseqid+"\n"
		del OB
	elif BL.qstart > BL.qend:
		OB=BODY
		del BODY
		BODY=OB+BL.qseqid+"\tblastn\tgene\t"+BL.qstart+"\t"+BL.qend+"\t.\t+\t.\t"+"ID="+BL.sseqid+"\n"
		del OB
	else:
		print "# poor record", BL.qstart, BL.qend


out=open(stem,'w')
out.write(HEADER)
out.write(BODY)
out.write("###")
out.close()









