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
		self.qstart=int(qstart)
		self.qend=int(qend)
		self.qlen=int(qlen)
		self.slen=int(slen)

f=open(HANDLE,"r")
#Currently not using a write to file option just sending all to stout
#stem=STEM_MAKER(HANDLE,".align.fasta")
#out=open(stem,"a")

Chrom=""
counter=0
for Line in f:
	SLine=Line.split()

	if SLine>=7:
		BL=blast_line(SLine[0],SLine[1],SLine[2],SLine[3],SLine[4],SLine[5])
	else:
		break
	if Chrom !=BL.qseqid:
		print "track name=\"" +Chrom+ "\" description=\"Some Description\" useScore=1"
		Chrom=BL.qseqid
		counter+=1
	if BL.qstart < BL.qend:
		print "chr"+str(counter), str( BL.qstart -1), str(BL.qend), str(BL.sseqid), "1000 +"
		
	elif BL.qstart > BL.qend:
		print "chr"+str(counter), str( BL.qend -1 ), str(BL.qstart), str(BL.sseqid), "1000 -"
	else:
		print "# poor record", BL.qstart, BL.qend












