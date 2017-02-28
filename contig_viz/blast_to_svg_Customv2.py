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
parser.add_argument("STEM", help="STEM for output gene files ")
args=parser.parse_args()
HANDLE=args.HANDLE0
STEM=args.STEM



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
	def __init__(self, qseqid, sseqid, qstart, qend, qlen, slen,gene,orient):
		self.qseqid=qseqid
		self.sseqid=sseqid
		self.qstart=qstart
		self.qend=qend
		self.qlen=qlen
		self.slen=slen
		self.orient=orient
		self.gene=gene
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#		Some Big variabled for svg11

#			Notice  view box is smallish 504 set in variable View_Max, all numbsers will be scaled to this View_Max variable.
#			Also of note in Header svg size limits number of annontations to ~200. This was just a hacky way to save time. More work could be done to tailor svg to acutal size.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#		Color Dictionary

COLOR_DICT={"trnY":"liceblue"
,"trnN":"orangered"
,"trnC":"aqua"
,"ccmC":"aquamarine"
,"atp4":"skyblue"
,"nad4L":"rosybrown"
,"atp8":"purple"
,"coxIII":"black"
,"rpl5":"saddlebrown"
,"trnD":"blue"
,"trnK":"blueviolet"
,"ccmB":"brown"
,"rpl10":"burlywood"
,"trnM":"cadetblue"
,"trnG":"chartreuse"
,"trnQ":"chocolate"
,"trnH":"coral"
,"trnE":"cornflowerblue"
,"coxI":"mediumorchid"
,"nad5":"crimson"
,"atp9":"cyan"
,"rps4":"darkblue"
,"rrn26":"darkcyan"
,"rrn5":"darkgoldenrod"
,"rrn18":"darkgray"
,"rps13":"darkgreen"
,"nad6":"sienna"
,"trnP":"darkkhaki"
,"trnF":"darkmagenta"
,"trnS":"darkolivegreen"
,"cob":"darkorange"
,"ccmFc":"darkorchid"
,"orf873":"darkred"
,"atp1":"darksalmon"
,"ccmFn":"darkseagreen"
,"ccmFn":"darkslateblue"
,"rpl16":"darkslategray"
,"matR":"darkslategrey"
,"nad3":"darkturquoise"
,"rps12":"darkviolet"
,"nad9":"deeppink"
,"trnW":"deepskyblue"
,"atp6":"dimgray"
,"trnK":"dimgrey"
}

#expanded list for heinous Zea mays genome

COLOR_DICT={"atp1-a1":"liceblue"
,"atp1-a2":"liceblue"
,"cp":"darkgreen"
,"ndhJ":"brightgreen"
,"psaA":"brightgreen"
,"rps4":"brightgreen"
,"ycf3":"brightgreen"
,"rbcL":"brightgreen"
,"psaB":"brightgreen"
,"psbA":"brightgreen"
,"psbD":"brightgreen"
,"psaA":"brightgreen"
,"atpA":"brightgreen"
,"atpF":"brightgreen"
,"ndhK":"brightgreen"
,"ndhJ":"brightgreen"
,"ndhJ":"brightgreen"
,"rps12":"brightgreen"
,"rps12":"brightgreen"
,"rps16":"brightgreen"
,"ycf3":"brightgreen"
,"ndhA":"brightgreen"
,"rpl14":"brightgreen"
,"atpF":"brightgreen"
,"atp4":"liceblue"
,"atp6":"liceblue"
,"atp8":"liceblue"
,"atp9":"liceblue"
,"ccmB":"bisque"
,"ccmC":"bisque"
,"ccmFC":"bisque"
,"ccmFN":"bisque"
,"cob":"blueviolet"
,"cox1":"brown"
,"cox2":"brown"
,"cox3":"brown"
,"mat-r":"deepgray"
,"nad1":"coral"
,"nad2":"coral"
,"nad3":"coral"
,"nad4":"coral"
,"nad4L":"coral"
,"nad5":"coral"
,"nad6":"coral"
,"nad7":"coral"
,"nad9":"coral"
,"ndhB-ct":"darkgreen"
,"rbcL-ct":"darkgreen"
,"rpl16":"chartreuse"
,"rpl2-ct":"chartreuse"
,"rpl23-ct":"chartreuse"
,"rps1":"darkblue"
,"rps12":"darkblue"
,"rps12-ct":"green"
,"rps13":"darkblue"
,"rps19":"darkblue"
,"rps2A":"darkblue"
,"rps2B":"darkblue"
,"rps3":"darkblue"
,"rps4":"darkblue"
,"rps7":"darkblue"
,"rps7-ct":"darkblue"
,"rrn16-ct":"darkmagenta"
,"rrn18":"darkmagenta"
,"rrn26":"darkmagenta"
,"rrn5":"darkmagenta"
,"trnC-ct":"firebrick"
,"trnD":"firebrick"
,"trnD-a1":"firebrick"
,"trnD-a2":"firebrick"
,"trnE-a1":"firebrick"
,"trnE-a2":"firebrick"
,"trnF-ct":"firebrick"
,"trnH-ct":"firebrick"
,"trnI-a1":"firebrick"
,"trnI-a2":"firebrick"
,"trnI-ct":"firebrick"
,"trnK":"firebrick"
,"trnL-a":"firebrick"
,"trnL-b":"firebrick"
,"trnL-c-ct":"firebrick"
,"trnM":"firebrick"
,"trnN-a1-ct":"firebrick"
,"trnN-a2-ct":"firebrick"
,"trnP-a1":"firebrick"
,"trnP-a2":"firebrick"
,"trnQ":"firebrick"
,"trnR-a":"firebrick"
,"trnR-b-ct":"firebrick"
,"trnS-a":"firebrick"
,"trnS-b":"firebrick"
,"trnV-ct":"firebrick"
,"trnY":"firebrick"
,"trnfM":"firebrick",
"trna":"firebrick"
}

# color dict for Marchantia

##COLOR_DICT={"atp1":"liceblue"
##,"atp4":"antiquewhite"
##,"atp6":"aqua"
##,"atp8":"aquamarine"
##,"atp9":"azure"
##,"ccmB":"beige"
##,"ccmC":"bisque"
##,"ccmF":"black"
##,"cob":"blanchedalmond"
##,"cox1":"blue"
##,"cox2":"blueviolet"
##,"cox3":"brown"
##,"nad1":"burlywood"
##,"nad2":"cadetblue"
##,"nad3":"chartreuse"
##,"nad4":"chocolate"
##,"nad4L":"coral"
##,"nad5":"cornflowerblue"
##,"nad6":"cornsilk"
##,"nad7":"crimson"
##,"nad9":"cyan"
##,"orf100":"darkblue"
##,"orf1065":"darkcyan"
##,"orf109":"darkgoldenrod"
##,"orf116":"darkgray"
##,"orf136":"darkgreen"
##,"orf139":"darkgrey"
##,"orf146":"darkkhaki"
##,"orf154":"darkmagenta"
##,"orf155":"darkolivegreen"
##,"orf167":"darkorange"
##,"orf168":"darkorchid"
##,"orf172":"darkred"
##,"orf180":"darksalmon"
##,"orf196":"darkseagreen"
##,"orf207":"darkslateblue"
##,"orf224":"darkslategray"
##,"orf264":"darkslategrey"
##,"orf302":"darkturquoise"
##,"orf502":"darkviolet"
##,"orf60":"deeppink"
##,"orf61":"deepskyblue"
##,"orf62":"dimgray"
##,"orf63":"dimgrey"
##,"orf64":"dodgerblue"
##,"orf681":"firebrick"
##,"orf69":"floralwhite"
##,"orf74":"forestgreen"
##,"orf742":"fuchsia"
##,"orf743":"gainsboro"
##,"orf79":"ghostwhite"
##,"orf86":"gold"
##,"orf887":"goldenrod"
##,"orf909":"gray"
##,"orf949":"grey"
##,"orf99":"green"
##,"rnl":"greenyellow"
##,"rns":"honeydew"
##,"rpl16":"hotpink"
##,"rpl2":"indianred"
##,"rpl5":"indigo"
##,"rpl6":"ivory"
##,"rps1":"khaki"
##,"rps10":"lavender"
##,"rps11":"lavenderblush"
##,"rps12":"lawngreen"
##,"rps13":"lemonchiffon"
##,"rps14":"lightblue"
##,"rps19":"lightcoral"
##,"rps2":"lightcyan"
##,"rps3":"lightgoldenrodyellow"
##,"rps4":"lightgray"
##,"rps7":"lightgreen"
##,"rps8":"lightgrey"
##,"rrn5":"lightpink"
##,"rtl":"lightsalmon"
##,"sdh3":"lightseagreen"
##,"sdh4":"lightskyblue"
##,"tatC":"lightslategray"
##,"trnA(ugc)":"lightslategrey"
##,"trnC(gca)":"lightsteelblue"
##,"trnD(guc)":"lightyellow"
##,"trnE(uuc)":"lime"
##,"trnF(gaa)":"limegreen"
##,"trnG(gcc)":"linen"
##,"trnG(ucc)":"magenta"
##,"trnH(gug)":"maroon"
##,"trnI(cau)":"mediumaquamarine"
##,"trnK(uuu)":"mediumblue"
##,"trnL(caa)":"mediumorchid"
##,"trnL(uaa)":"mediumpurple"
##,"trnL(uag)":"mediumseagreen"
##,"trnM(cau)e":"mediumslateblue"
##,"trnM(cau)f":"mediumspringgreen"
##,"trnN(guu)":"mediumturquoise"
##,"trnP(ugg)":"mediumvioletred"
##,"trnQ(uug)":"midnightblue"
##,"trnR(acg)":"mintcream"
##,"trnR(ucg)":"mistyrose"
##,"trnR(ucu)":"moccasin"
##,"trnS(gcu)":"navajowhite"
##,"trnS(uga)":"navy"
##,"trnT(ggu)":"oldlace"
##,"trnV(uac)":"olive"
##,"trnW(cca)":"olivedrab"
##,"trnY(gua)":"orange"
##}





f=open(HANDLE,"r")
#Currently not using a write to file option just sending all to stout
#stem=STEM_MAKER(HANDLE,".align.fasta")
#out=open(stem,"a")
CUSTOM_SORT={"atp1-a1":[],"atp1-a2":[],"atp4":[],"atp6":[],"atp8":[],"atp9":[],"ccmB":[],"ccmC":[],"ccmFC":[],"ccmFN":[],"cob":[],"cox1":[],"cox2":[],"cox3":[],"mat-r":[],"nad1":[],"nad2":[],"nad3":[],"nad4":[],"nad4L":[],"nad5":[],"nad6":[],"nad7":[],"nad9":[],"ndhB-ct":[],"rbcL-ct":[],"rpl16":[],"rpl2-ct":[],"rpl23-ct":[],"rps1":[],"rps12":[],"rps12-ct":[],"rps13":[],"rps19-ct":[],"rps2A":[],"rps2B":[],"rps3":[],"rps4":[],"rps7":[],"rps7-ct":[],"rrn16-ct":[],"rrn18":[],"rrn26":[],"rrn5":[],"cp":[]}
ADDED={"atp1-a1":[],"atp1-a2":[],"atp4":[],"atp6":[],"atp8":[],"atp9":[],"ccmB":[],"ccmC":[],"ccmFC":[],"ccmFN":[],"cob":[],"cox1":[],"cox2":[],"cox3":[],"mat-r":[],"nad1":[],"nad2":[],"nad3":[],"nad4":[],"nad4L":[],"nad5":[],"nad6":[],"nad7":[],"nad9":[],"ndhB-ct":[],"rbcL-ct":[],"rpl16":[],"rpl2-ct":[],"rpl23-ct":[],"rps1":[],"rps12":[],"rps12-ct":[],"rps13":[],"rps19-ct":[],"rps2A":[],"rps2B":[],"rps3":[],"rps4":[],"rps7":[],"rps7-ct":[],"rrn16-ct":[],"rrn18":[],"rrn26":[],"rrn5":[],"cp":[]}
# Custom and Added have been updated to match current set of genes detected using a mazie annotation. 





GENE_LIST=[]
Genome=[]
Contig=[]
MAXY=[] # max contig lenght
Max_Contig_name=[]
Chrom=""
counter=0
for Line in f:
	SLine=Line.split()

	if SLine>=7:
		BL=blast_line(SLine[0],SLine[1],int(SLine[2]),int(SLine[3]),int(SLine[4]),int(SLine[5]),"Null","Null")
	else:
		break
	if Chrom !=BL.qseqid:
		#print "track name=\"" +Chrom+ "\" description=\"Some Description\" useScore=1"
		Chrom=BL.qseqid
		Genome.append(sorted(Contig, key=lambda X : X.qstart))
		if counter>0:
			MAXY.append(Contig[0].qlen)
			Max_Contig_name.append(len(BL.qseqid))
			for GENE in set(GENE_LIST):
				#print GENE
				if GENE in CUSTOM_SORT and len(Contig)>2 and Contig[0].qseqid not in ADDED[GENE]:
					#print GENE , "ADDED"
					CUSTOM_SORT[GENE].append(sorted(Contig, key=lambda X : X.qstart))
					ADDED[GENE].append(Contig[0].qseqid)
			del GENE_LIST
			GENE_LIST=[]
		del Contig
		Contig=[]
		counter+=1
	elif BL.qstart < BL.qend:
		#print "chr"+str(counter), BL.qstart, BL.qend, BL.sseqid, "1000 +"
		BL.orient="+"
		
		
	elif BL.qstart > BL.qend:
		#print "chr"+str(counter), BL.qend, BL.qstart, BL.sseqid, "1000 -"
		BL.orient="-"
		start=BL.qend
		end=BL.qstart
		BL.qend=end
		BL.qstart=start
		
	else:
		print "# poor record", BL.qstart, BL.qend
	Contig.append(BL)
	gene_parse=(BL.sseqid.split(":"))[1]
	BL.gene=gene_parse
	GENE_LIST.append(BL.gene)

for GENE in GENE_LIST:
	##print GENE
	if GENE in CUSTOM_SORT:
		##print GENE , "ADDED"
		CUSTOM_SORT[GENE].append(sorted(Contig, key=lambda X : X.qstart))

Genome.append(sorted(Contig, key=lambda X : X.qstart))
MAXY.append(Contig[0].qlen)
Max_Contig_name.append(len(BL.qseqid))

#for Contig in Genome:
#	if len(Contig)>0:
#		print Contig[0].qseqid
#		for BL in Contig:
#			print BL.qstart, BL.qend







for GENE in CUSTOM_SORT:

	fout=open(STEM+"_"+GENE+".svg", "w")
	Last_Anch=0.0
	Comp=0.0
	Text_spacer=11.1
	View_Max=1200
	Max_CON=float(max(MAXY))+20
	Max_Name=float(max(Max_Contig_name))
	Scale_factor=(View_Max-(20+Max_Name*12))/(Max_CON )

	old_counter=300

	Header="""<?xml version="1.0" encoding="UTF-8"?>
	<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%ipt" height="%ipt" viewBox="-50 0 %i %i" version="1.1">
	""" %(View_Max,len(CUSTOM_SORT[GENE])*old_counter+old_counter, View_Max,len(CUSTOM_SORT[GENE])*old_counter+old_counter)
	fout.write(Header) 
		#print GENE, CUSTOM_SORT[GENE]
	for Fragment in CUSTOM_SORT[GENE]:
		fout.write( "<g>")

	
		del BL
		readable=0
		Last_Anch=0
		for BL in Fragment:
		
		
			Comp=(BL.qstart*Scale_factor)-Last_Anch
			######print "\n\n\t\t"+str(Comp),  Comp <=Text_spacer,"\n\n\t\t"
			if Comp <Text_spacer:
			
				readable+=Text_spacer

			else:
				readable=0
			########print "\n\n\n\t\t\t", Comp, readable, Last_Anch, Text_spacer,(BL.qstart*Scale_factor), "\n\n\n\t\t\t"
			fout.write(  "<rect x = \"%f\" y = \"%f\" width = \"%f\" height = \"22\" fill = \"%s\" stroke = \"black\" stroke-width = \"0.0005\" />" %( float(BL.qstart)*Scale_factor, (old_counter-10),    (int(BL.qend)-int(BL.qstart))*Scale_factor, COLOR_DICT[BL.gene]))

			fout.write("<text x=\"%f\" y=\"%i\" transform=\"rotate(270,%f,%i)\" font-size=\"11\" >%s</text>" %((float(BL.qstart))*Scale_factor+readable,(old_counter-12),float(BL.qstart)*Scale_factor+readable,(old_counter-12),BL.gene))
			Last_Anch=float(BL.qstart)*Scale_factor+readable
##		Statement to print line connencting offset text if it is outside the boundaries of the box.
			if (int(BL.qend)-int(BL.qstart))*Scale_factor+BL.qstart*Scale_factor < (float(BL.qstart))*Scale_factor+readable and Comp <=Text_spacer:  ####for skinny boxes draw line to text
				fout.write("<line x1=\"%i\" y1=\"%i\" x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"01\" stroke-opacity = \"0.7\" />" %(float(BL.qstart)*Scale_factor+(((int(BL.qend)-int(BL.qstart))*Scale_factor)/1.0),  old_counter-10 , float(BL.qstart)*Scale_factor+readable, old_counter-12))
		BL=Fragment[0]
		fout.write( "<line x1=\"0\" y1=\"%i\" x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"1\"/>" %(old_counter, int(BL.qlen)*Scale_factor  , old_counter))
		fout.write( "<text x=\"%i\" y=\"%i\" font-size=\"11\" >%s                        </text>" %(int(BL.qlen)*Scale_factor+10,(old_counter),BL.qseqid))
	
		for X in range(0,BL.qlen,1000):
			fout.write("<line x1=\"%i\" y1=\"%i\"  x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"0.25\"/>" %(X*Scale_factor,old_counter+2 ,X*Scale_factor, old_counter))		
		for X in range(0,BL.qlen,5000):
			fout.write("<line x1=\"%i\" y1=\"%i\"  x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"0.5\"/>" %(X*Scale_factor,old_counter+4 ,X*Scale_factor, old_counter))
		for X in range(0,BL.qlen,10000):
			fout.write("<line x1=\"%i\" y1=\"%i\"  x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"0.75\"/>" %(X*Scale_factor,old_counter+8 ,X*Scale_factor, old_counter))
		fout.write("</g>")
		if BL.qstart > BL.qend:
			print "ERROR"
		old_counter+=150
		

	fout.write("</svg>")
	fout.close()
		
		












