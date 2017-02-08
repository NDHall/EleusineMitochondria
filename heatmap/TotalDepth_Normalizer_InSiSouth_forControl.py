#!/usr/bin/python

#IMPORTANT NOTES



#written for Python 2.7.1


import argparse
import re

#class blast_line:
#	def __init__(self, qseqid, sseqid, qstart, qend, qlen, slen):
#		self.qseqid=qseqid
#		self.sseqid=sseqid
#		self.qstart=qstart
#		self.qend=qend
#		self.qlen=qlen
#		self.slen=slen



class IDXStats:
	def __init__(self,SRA,Gene,Exon,Genome,Length,Reads, RdivL,Norm_RdivL):
		self.SRA=SRA
		self.Gene=Gene
		self.Exon=Exon
		self.Genome=Genome
		self.Length=Length
		self.Reads=Reads
		self.RL=RdivL
		self.NormRL=Norm_RdivL

class DepthLine:
	def __init__(self, SRA, Gene, Exon, Genome, Pos, Depth, AdDepth ):
		self.SRA=SRA
		self.Gene=Gene
		self.Exon=Exon
		self.Genome=Genome
		self.Pos=Pos
		self.Depth=Depth
		self.AdDepth=AdDepth

#	house keeping


def clean_for_append(out):
	f=open(out,'w')
	f.write("")
	f.close()

#----------------------------------------------------------------------------------------------------------------

# line parsing for output os Souther_runner.sh 
# The input could be manipulated to take straight samtools output. But would need new function to do so. 


def IdxStats_ParserII(Line,EXCLUDE,FileName):
	if EXCLUDE not in Line:
		Pline=Line.replace("###"," ")
		Pline=Pline.split(" ")
		if len(Pline) >=2 :
			if "_" in Pline[1]:
				gene_name=Pline[1].split("_")[0]
			else:
				gene_name=Pline[1]
#		print Pline
		StatLine=IDXStats(Pline[0],gene_name,Pline[1],FileName, int(Pline[2]),int(Pline[3]),float(Pline[3])/float(Pline[2]), "Null")
	else:
		StatLine="Null"

	return StatLine

def Depth_ParserII(Line , FileName):

	Pline=Line.split(" ")
	if "_" in Pline[1]:
		gene_name=Pline[1].split("_")[0]
	else:
		gene_name=Pline[1]
	DL=DepthLine(Pline[0],gene_name,Pline[1],FileName,int(Pline[2]),int(Pline[3]),0)
	return DL




# Xargs area. 


parser=argparse.ArgumentParser()
parser.add_argument("ControlIdxStats", help="samtools IDXstats output for Control bam")
parser.add_argument("Control",help="samtools depth output for Control file. The file that will determine what 1 fold is. Modified to include column indicating SRA of origin")
parser.add_argument("CDSIDX", help="samtools idx output for CDS fille")
parser.add_argument("CDSDepth", help="samtools depth output. Modified to include column indicating SRA of origin")


args=parser.parse_args()

IDX=args.ControlIdxStats
CONTROL=args.Control
CDS_DEPTH=args.CDSDepth
CDS_IDX=args.CDSIDX


idx=open(IDX,"r")

SeqStat={}

for Line in idx:
	Parsed=IdxStats_ParserII(Line, "*",IDX)
	if Parsed !="Null":
##		print Parsed.Gene, Parsed.SRA, Parsed.Exon, Parsed.Genome, Parsed.Length, Parsed.Reads, Parsed.RL, Parsed.NormRL
		if "*" not in Parsed.Exon :
			Message="SRA sets must occur only once per Genome. \n\t"+Parsed.Genome+"\t"+Parsed.SRA
			assert(Parsed.SRA not in SeqStat),Message
			SeqStat[Parsed.Exon]=Parsed
tmpDict={}

# Limit to Control to Known genes. Added to ensure fidelity of genes. used to calculate gene Averages
for X in SeqStat:
	ADD=False
	
	if "nad7" in SeqStat[X].Exon:
		#print SeqStat[X].Exon
		ADD=True
	elif "nad4" in SeqStat[X].Exon and "nad4L" not in SeqStat[X].Exon :
		#print SeqStat[X].Exon
		ADD=True
	elif "matR" in SeqStat[X].Exon:
		#print SeqStat[X].Exon
		ADD=True
	if ADD is True:
		tmpDict[X]=SeqStat[X]
SeqStat=tmpDict


#print tmpDict

#for X in SeqStat:
	#print SeqStat[X].Exon , SeqStat[X].Length




# This set of commands adds all control genes to a Dictionary 


TD_dict={}

for TotalLine in open(CONTROL,"r"):
##	print TotalLine
	TD=Depth_ParserII(TotalLine,CONTROL)
	if TD.Exon not in TD_dict:
		TD_dict[TD.Exon]=[[TD.Pos],[TD.Depth]]
	elif TD.Exon in TD_dict:
		TD_dict[TD.Exon][0].append(TD.Pos)
		TD_dict[TD.Exon][1].append(TD.Depth)
		
	else :
		raise Exception("Improperly formated File: "+DEPTH+"\n\tOffending Line:\n\t"+TotalLine)

#----------------------------------------------------------------------------------------

# Dictonary of ControlIDXStats is used to calculate  Mean per gene, along with number of gaps in map. 
# Now lets normalize. lets first start by getting a gene wide average for coverage.


#----------------------------------------------------------------------------------------


NormLevel={}


for EXON in SeqStat:
#	print EXON
	IDX=SeqStat[EXON]
	DP=0
	Counter=0
	
#	print len([IDX.Exon][1])
	for NUM in TD_dict[IDX.Exon][1]:
##		print Counter, NUM, IDX.Exon, IDX.SRA
		DP+=NUM
		Counter+=1
##		print DP,NUM 
	Message="Normalizing gene must only ever appear once per Control file for them to be valid\n\tOffending Values:  "+IDX.Exon
	assert( EXON not in NormLevel),Message

	
	Avg=float(DP)/float(Counter) 		# Note this statment only averages depth of mapped position. Different from Other version TotalDepth_Normalized_inSilicoSouth.py
	NoCov=IDX.Length-Counter
	NormLevel[EXON]=[Avg,NoCov]
Normalizer=0
AvgGaps=0
Counter=0
for X in NormLevel:
	Normalizer+= NormLevel[X][0]
	AvgGaps+= NormLevel[X][1]
	Counter+=1
#	print NormLevel[X][0]
Normalizer=float(Normalizer)/float(Counter)
AvgGaps=float(AvgGaps)/float(Counter)
#print "Normalizer and gaps", Normalizer, AvgGaps

#------------------------------------------------------------------


# Now add IDX stats for CDS Examination

Tot_CDS={}


cds_idx= open(CDS_IDX, "r")

for Line in cds_idx:
	Parsed=IdxStats_ParserII(Line, "*",cds_idx)
	if Parsed !="Null":
##		print Parsed.Gene, Parsed.SRA, Parsed.Exon, Parsed.Genome, Parsed.Length, Parsed.Reads, Parsed.RL, Parsed.NormRL
		if "*" not in Parsed.Exon :
			Message="SRA sets must occur only once per Genome. \n\t"+str(Parsed.Genome)+"\t"+str(Parsed.SRA)
			assert(Parsed.Exon not in Tot_CDS),Message
			Tot_CDS[Parsed.Exon]=Parsed
#for X in Tot_CDS:
#	print X, Tot_CDS[X].Length, Tot_CDS[X].Reads

##------------------------------------------------------------------------------

#	Now Parse Depth for All CDSDepth


##-------------------------------------------------------------------------------

del TD_dict

TD_dict={}

for TotalLine in open(CDS_DEPTH,"r"):
##	print TotalLine
	TD=Depth_ParserII(TotalLine,CONTROL)
	if TD.Exon not in TD_dict:
		TD_dict[TD.Exon]=[[TD.Pos],[TD.Depth]]
	elif TD.Exon in TD_dict:
		TD_dict[TD.Exon][0].append(TD.Pos)
		TD_dict[TD.Exon][1].append(TD.Depth)
		
	else :
		raise Exception("Improperly formated File: "+DEPTH+"\n\tOffending Line:\n\t"+TotalLine)

##for X in TD_dict :
###	print X ,"TD_dict"

#--------------------------------------------------------------------------------------------------------------

##	At this point we have
##	2. dictionaries that contain Length and Depth information for each gene.
##	These dictionaries can be joined on the Exon value used as key for each 
##	entry.
##	Now we will output Trace file and Summary table for these accession.
##	Trace file will be modified Depth Table with values adjusted.
##	Summary of fold and No coverage sites for each gene will put out in HeatMap table. 
##	
##	While I intially wrote this script for 4 files. Above filtering steps for creating variable Normalized allow for Controls
##	To be imbedded in the actual CDS file at Large. This is best. It also means that Entry names must be strictly curates and matched to 
##	filtering for IDX and Normalizing  steps.

#---------------------------------------------------------------------------------------------------------------



# Trace files.

for KEY  in NormLevel:
	if 'nad7' in KEY:
		N7=NormLevel[KEY][0]
	elif  'nad4' in KEY:
		N4=NormLevel[KEY][0]
	elif 'matR' in KEY:
		MR=NormLevel[KEY][0]


clean_for_append("ADJ_"+CDS_DEPTH)

TraceOut=open("ADJ_"+CDS_DEPTH, 'a')
CDS_AVG={}
TraceOut.write( "SRA Exon Genome Pos DP ADP AvgCovOf_nad7 AvgCovOf_nad4 AvgCovOf_matR\n")
for EXON in TD_dict:
	Raw=0
	Adj=0
	Counter=0
	for  POS, DEPTH in zip(TD_dict[EXON][0],TD_dict[EXON][1]):
		# get Averages out NormLevel Dictionar

		TraceOut.write( " ".join([Tot_CDS[EXON].SRA,EXON, CDS_DEPTH, str(POS), str(DEPTH), str(float(DEPTH)/float(Normalizer)),str(Normalizer),str(N7),str(N4),str(MR)]))
		TraceOut.write("\n")
		Raw+=DEPTH
		Adj+=(float(DEPTH)/float(Normalizer))
		Counter+=1
	Message="Exons must occur once and have uniq names"
	assert( EXON not in CDS_AVG),Message
	AvgRaw=float(Raw)/float(Counter)
	AvgAdj=float(Adj)/float(Counter)
	NoGaps=Tot_CDS[EXON].Length - Counter # number of Positions mapped subtracted from length of seq reported in IDX stats
	CDS_AVG[EXON]=[AvgRaw, AvgAdj, NoGaps]


		

clean_for_append("Summary_"+CDS_DEPTH)

SUMMARY=open("Summary_"+CDS_DEPTH, 'a')


SUMMARY_LIST=[]

for EXON in Tot_CDS:
	if EXON not in CDS_AVG:
		toAppend=[ Tot_CDS[EXON].SRA, EXON, Tot_CDS[EXON].Length, 0, 0, Tot_CDS[EXON].Length]
	elif EXON in CDS_AVG:
		toAppend=[ Tot_CDS[EXON].SRA, EXON,  Tot_CDS[EXON].Length, CDS_AVG[EXON][0], CDS_AVG[EXON][1], CDS_AVG[EXON][2] ]
	stringToAppend=[]
	for ELEMENT in toAppend:
		stringToAppend.append(str(ELEMENT))
	SUMMARY_LIST.append(stringToAppend)

for X in SUMMARY_LIST:
	SUMMARY.write( " ".join(X)+"\n")

idx.close()
TraceOut.close()
SUMMARY.close()
cds_idx.close()





































