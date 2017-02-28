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
# expanded  list of genes added for heinous Maize genome.


COLOR_DICT={"atp1-a1":"liceblue"
,"atp1-a2":"antiquewhite"
,"atp4":"aqua"
,"atp6":"aquamarine"
,"atp8":"azure"
,"atp9":"beige"
,"ccmB":"bisque"
,"ccmC":"black"
,"ccmFC":"blanchedalmond"
,"ccmFN":"blue"
,"cob":"blueviolet"
,"cox1":"brown"
,"cox2":"burlywood"
,"cox3":"cadetblue"
,"mat-r":"chartreuse"
,"nad1":"chocolate"
,"nad2":"coral"
,"nad3":"cornflowerblue"
,"nad4":"cornsilk"
,"nad4L":"crimson"
,"nad5":"cyan"
,"nad6":"darkblue"
,"nad7":"darkcyan"
,"nad9":"darkgoldenrod"
,"ndhB-ct":"darkgray"
,"orf100-a":"darkgreen"
,"orf100-a1":"darkgrey"
,"orf100-a2":"darkkhaki"
,"orf100-b-ct":"darkmagenta"
,"orf100-c":"darkolivegreen"
,"orf101-a":"darkorange"
,"orf101-b":"darkorchid"
,"orf101-c":"darkred"
,"orf102-a":"darksalmon"
,"orf102-b":"darkseagreen"
,"orf104-a":"darkslateblue"
,"orf104-b":"darkslategray"
,"orf105-a":"darkslategrey"
,"orf105-b":"darkturquoise"
,"orf105-c":"darkviolet"
,"orf105-d":"deeppink"
,"orf105-e":"deepskyblue"
,"orf105-f":"dimgray"
,"orf105-g":"dimgrey"
,"orf106":"dodgerblue"
,"orf106-a1":"firebrick"
,"orf106-a2":"floralwhite"
,"orf106-b":"forestgreen"
,"orf106-c":"fuchsia"
,"orf107-a":"gainsboro"
,"orf107-b":"ghostwhite"
,"orf107-c":"gold"
,"orf107-d":"goldenrod"
,"orf109":"gray"
,"orf109-a":"grey"
,"orf109-b-ct":"green"
,"orf110-a":"greenyellow"
,"orf110-b":"honeydew"
,"orf110-c":"hotpink"
,"orf111-a":"indianred"
,"orf111-b":"indigo"
,"orf112-a1":"ivory"
,"orf112-a2":"khaki"
,"orf113-a":"lavender"
,"orf113-b":"lavenderblush"
,"orf114-a":"lawngreen"
,"orf114-b":"lemonchiffon"
,"orf115-a1":"lightblue"
,"orf115-a2":"lightcoral"
,"orf115-b":"lightcyan"
,"orf115-c1":"lightgoldenrodyellow"
,"orf115-c2":"lightgray"
,"orf115-d":"lightgreen"
,"orf115-e":"lightgrey"
,"orf1159":"lightpink"
,"orf116-a":"lightsalmon"
,"orf116-b":"lightseagreen"
,"orf117-a":"lightskyblue"
,"orf117-b":"lightslategray"
,"orf117-c":"lightslategrey"
,"orf117-d":"lightsteelblue"
,"orf118":"lightyellow"
,"orf119-a":"lime"
,"orf119-b":"limegreen"
,"orf119-c":"linen"
,"orf120":"magenta"
,"orf121-a-ct":"maroon"
,"orf121-b":"mediumaquamarine"
,"orf121-c":"mediumblue"
,"orf122":"mediumorchid"
,"orf125":"mediumpurple"
,"orf126-a":"mediumseagreen"
,"orf126-b1":"mediumslateblue"
,"orf126-b2":"mediumspringgreen"
,"orf126-c":"mediumturquoise"
,"orf126-d":"mediumvioletred"
,"orf127":"midnightblue"
,"orf128":"mintcream"
,"orf129-a":"mistyrose"
,"orf129-b":"moccasin"
,"orf130":"navajowhite"
,"orf131-a":"navy"
,"orf131-b-ct":"oldlace"
,"orf131-c":"olive"
,"orf132":"olivedrab"
,"orf133-a":"orange"
,"orf133-b":"orangered"
,"orf134-a-ct":"orchid"
,"orf134-b":"palegoldenrod"
,"orf135":"palegreen"
,"orf137-a-ct":"paleturquoise"
,"orf137-b":"palevioletred"
,"orf138-a":"papayawhip"
,"orf138-b":"peachpuff"
,"orf140-a":"peru"
,"orf140-b":"pink"
,"orf140-c":"plum"
,"orf140-ct":"powderblue"
,"orf145":"purple"
,"orf146-a":"red"
,"orf146-ct":"rosybrown"
,"orf147-a":"royalblue"
,"orf147-b":"saddlebrown"
,"orf149-a":"salmon"
,"orf149-b":"sandybrown"
,"orf158-a1":"seagreen"
,"orf158-a2":"seashell"
,"orf160-a":"sienna"
,"orf161":"silver"
,"orf163":"skyblue"
,"orf165":"slateblue"
,"orf179":"slategray"
,"orf186":"slategrey"
,"orf191":"snow"
,"orf193-a1":"springgreen"
,"orf193-a2":"steelblue"
,"orf206":"tan"
,"orf227-ct":"teal"
,"orf247-ct":"thistle"
,"orf248":"tomato"
,"orf261":"turquoise"
,"orf275":"violet"
,"orf302":"wheat"
,"orf342":"white"
,"orf387":"whitesmoke"
,"orf396":"yellow"
,"orf417":"yellowgreen"
,"orf444":"liceblue"
,"orf734":"antiquewhite"
,"orf911":"aqua"
,"orf99-a1":"aquamarine"
,"orf99-a2":"azure"
,"orf99-b1":"beige"
,"orf99-b2":"bisque"
,"orf99-c":"black"
,"orf99-d":"blanchedalmond"
,"orf99-e":"blue"
,"orf99-f":"blueviolet"
,"orf99-g":"brown"
,"orfX":"burlywood"
,"rbcL-ct":"cadetblue"
,"rpl16":"chartreuse"
,"rpl2-ct":"chocolate"
,"rpl23-ct":"coral"
,"rps1":"cornflowerblue"
,"rps12":"cornsilk"
,"rps12-ct":"crimson"
,"rps13":"cyan"
,"rps19-ct":"darkblue"
,"rps2A":"darkcyan"
,"rps2B":"darkgoldenrod"
,"rps3":"darkgray"
,"rps4":"darkgreen"
,"rps7":"darkgrey"
,"rps7-ct":"darkkhaki"
,"rrn16-ct":"darkmagenta"
,"rrn18":"darkolivegreen"
,"rrn26":"darkorange"
,"rrn5":"darkorchid"
,"trnC-ct":"darkred"
,"trnD":"darksalmon"
,"trnD-a1":"darkseagreen"
,"trnD-a2":"darkslateblue"
,"trnE-a1":"darkslategray"
,"trnE-a2":"darkslategrey"
,"trnF-ct":"darkturquoise"
,"trnH-ct":"darkviolet"
,"trnI-a1":"deeppink"
,"trnI-a2":"deepskyblue"
,"trnI-ct":"dimgray"
,"trnK":"dimgrey"
,"trnL-a":"dodgerblue"
,"trnL-b":"firebrick"
,"trnL-c-ct":"floralwhite"
,"trnM":"forestgreen"
,"trnN-a1-ct":"fuchsia"
,"trnN-a2-ct":"gainsboro"
,"trnP-a1":"ghostwhite"
,"trnP-a2":"gold"
,"trnQ":"goldenrod"
,"trnR-a":"gray"
,"trnR-b-ct":"grey"
,"trnS-a":"green"
,"trnS-b":"greenyellow"
,"trnV-ct":"honeydew"
,"trnY":"hotpink"
,"trnfM":"indianred"
}

# color dict for Marchantia

COLOR_DICT={"atp1":"liceblue"
,"atp4":"antiquewhite"
,"atp6":"aqua"
,"atp8":"aquamarine"
,"atp9":"azure"
,"ccmB":"beige"
,"ccmC":"bisque"
,"ccmF":"black"
,"cob":"blanchedalmond"
,"cox1":"blue"
,"cox2":"blueviolet"
,"cox3":"brown"
,"nad1":"burlywood"
,"nad2":"cadetblue"
,"nad3":"chartreuse"
,"nad4":"chocolate"
,"nad4L":"coral"
,"nad5":"cornflowerblue"
,"nad6":"cornsilk"
,"nad7":"crimson"
,"nad9":"cyan"
,"orf100":"darkblue"
,"orf1065":"darkcyan"
,"orf109":"darkgoldenrod"
,"orf116":"darkgray"
,"orf136":"darkgreen"
,"orf139":"darkgrey"
,"orf146":"darkkhaki"
,"orf154":"darkmagenta"
,"orf155":"darkolivegreen"
,"orf167":"darkorange"
,"orf168":"darkorchid"
,"orf172":"darkred"
,"orf180":"darksalmon"
,"orf196":"darkseagreen"
,"orf207":"darkslateblue"
,"orf224":"darkslategray"
,"orf264":"darkslategrey"
,"orf302":"darkturquoise"
,"orf502":"darkviolet"
,"orf60":"deeppink"
,"orf61":"deepskyblue"
,"orf62":"dimgray"
,"orf63":"dimgrey"
,"orf64":"dodgerblue"
,"orf681":"firebrick"
,"orf69":"floralwhite"
,"orf74":"forestgreen"
,"orf742":"fuchsia"
,"orf743":"gainsboro"
,"orf79":"ghostwhite"
,"orf86":"gold"
,"orf887":"goldenrod"
,"orf909":"gray"
,"orf949":"grey"
,"orf99":"green"
,"rnl":"greenyellow"
,"rns":"honeydew"
,"rpl16":"hotpink"
,"rpl2":"indianred"
,"rpl5":"indigo"
,"rpl6":"ivory"
,"rps1":"khaki"
,"rps10":"lavender"
,"rps11":"lavenderblush"
,"rps12":"lawngreen"
,"rps13":"lemonchiffon"
,"rps14":"lightblue"
,"rps19":"lightcoral"
,"rps2":"lightcyan"
,"rps3":"lightgoldenrodyellow"
,"rps4":"lightgray"
,"rps7":"lightgreen"
,"rps8":"lightgrey"
,"rrn5":"lightpink"
,"rtl":"lightsalmon"
,"sdh3":"lightseagreen"
,"sdh4":"lightskyblue"
,"tatC":"lightslategray"
,"trnA(ugc)":"lightslategrey"
,"trnC(gca)":"lightsteelblue"
,"trnD(guc)":"lightyellow"
,"trnE(uuc)":"lime"
,"trnF(gaa)":"limegreen"
,"trnG(gcc)":"linen"
,"trnG(ucc)":"magenta"
,"trnH(gug)":"maroon"
,"trnI(cau)":"mediumaquamarine"
,"trnK(uuu)":"mediumblue"
,"trnL(caa)":"mediumorchid"
,"trnL(uaa)":"mediumpurple"
,"trnL(uag)":"mediumseagreen"
,"trnM(cau)e":"mediumslateblue"
,"trnM(cau)f":"mediumspringgreen"
,"trnN(guu)":"mediumturquoise"
,"trnP(ugg)":"mediumvioletred"
,"trnQ(uug)":"midnightblue"
,"trnR(acg)":"mintcream"
,"trnR(ucg)":"mistyrose"
,"trnR(ucu)":"moccasin"
,"trnS(gcu)":"navajowhite"
,"trnS(uga)":"navy"
,"trnT(ggu)":"oldlace"
,"trnV(uac)":"olive"
,"trnW(cca)":"olivedrab"
,"trnY(gua)":"orange"
}


#expanded list for heinous Zea mays genome

COLOR_DICT={"atp1-a1":"liceblue"
,"atp1-a2":"liceblue"
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
,"trnfM":"firebrick"
}


f=open(HANDLE,"r")
#Currently not using a write to file option just sending all to stout
#stem=STEM_MAKER(HANDLE,".align.fasta")
#out=open(stem,"a")
#CUSTOM_SORT={"matR":[],"rrn26":[], "ccmFn":[], "nad9":[], "nad6":[], "nad5":[], "rrn18":[], "coxIII":[] }
#ADDED={"matR":[],"rrn26":[], "ccmFn":[], "nad9":[], "nad6":[], "nad5":[], "rrn18":[], "coxIII":[] }
# Custom and Added have been updated to match current set of genes detected using a mazie annotation. 




f=open(HANDLE,"r")
#Currently not using a write to file option just sending all to stout
#stem=STEM_MAKER(HANDLE,".align.fasta")
#out=open(stem,"a")


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
		del Contig
		Contig=[]
		counter+=1
	if BL.qstart < BL.qend:
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


Genome.append(sorted(Contig, key=lambda X : X.qstart))
MAXY.append(Contig[0].qlen)
Max_Contig_name.append(len(BL.qseqid))

#for Contig in Genome:
#	if len(Contig)>0:
#		print Contig[0].qseqid
#		for BL in Contig:
#			print BL.qstart, BL.qend




# expanded View max  1/8/2016 from 1200 ->120000

View_Max=120000
Max_CON=float(max(MAXY))+20
Max_Name=float(max(Max_Contig_name))
Scale_factor=(View_Max-(20+Max_Name*12))/(Max_CON )

old_counter=1500

Header="""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%ipt" height="%ipt" viewBox="-50 0 %i %i" version="1.1">
""" %(View_Max,len(Genome)*old_counter+old_counter, View_Max,len(Genome)*old_counter+old_counter)
print Header 




Last_Anch=0.0

Comp=0.0
Text_spacer=11.1
for Contig in Genome:
	if len(Contig) >0:
		print "<g>"

		
		del BL
		readable=0
		Last_Anch=0
		for BL in Contig:
			
			Comp=(BL.qstart*Scale_factor)-Last_Anch
#			print "\n\n\t\t"+str(Comp),  Comp <=Text_spacer,"\n\n\t\t"
			if Comp <Text_spacer:
				
				readable+=Text_spacer

			else:
				readable=0
#			print "\n\n\n\t\t\t", Comp, readable, Last_Anch, Text_spacer,(BL.qstart*Scale_factor), "\n\n\n\t\t\t"
			if BL.gene in COLOR_DICT and BL.orient =="+":
				print   "<rect x = \"%f\" y = \"%f\" width = \"%f\" height = \"500\" fill = \"%s\" stroke = \"black\" stroke-width = \"0.0005\" />" %( float(BL.qstart)*Scale_factor, (old_counter-10),    (int(BL.qend)-int(BL.qstart))*Scale_factor, COLOR_DICT[BL.gene])

				print "<text x=\"%f\" y=\"%i\" transform=\"rotate(270,%f,%i)\" font-size=\"40\" >%s</text>" %((float(BL.qstart))*Scale_factor+readable,(old_counter-12),float(BL.qstart)*Scale_factor+readable,(old_counter-12),BL.gene)
			elif BL.gene in COLOR_DICT and BL.orient =="-":
				print   "<rect x = \"%f\" y = \"%f\" width = \"%f\" height = \"500\" fill = \"%s\" stroke = \"black\" stroke-width = \"0.0005\" />" %( float(BL.qstart)*Scale_factor, (old_counter+10),    (int(BL.qend)-int(BL.qstart))*Scale_factor, COLOR_DICT[BL.gene])

				print "<text x=\"%f\" y=\"%i\" transform=\"rotate(270,%f,%i)\" font-size=\"40\" >%s</text>" %((float(BL.qstart))*Scale_factor+readable,(old_counter+12),float(BL.qstart)*Scale_factor+readable,(old_counter+12),BL.gene)
			elif BL.gene not in COLOR_DICT and BL.orient =="+":
				print   "<rect x = \"%f\" y = \"%f\" width = \"%f\" height = \"500\" fill = \"%s\" stroke = \"black\" stroke-width = \"0.0005\" />" %( float(BL.qstart)*Scale_factor, (old_counter-10),    (int(BL.qend)-int(BL.qstart))*Scale_factor, "tomato")

				print "<text x=\"%f\" y=\"%i\" transform=\"rotate(270,%f,%i)\" font-size=\"40\" >%s</text>" %((float(BL.qstart))*Scale_factor+readable,(old_counter-12),float(BL.qstart)*Scale_factor+readable,(old_counter-12),BL.gene)
			elif BL.gene not in COLOR_DICT and BL.orient =="+":
				print   "<rect x = \"%f\" y = \"%f\" width = \"%f\" height = \"500\" fill = \"%s\" stroke = \"black\" stroke-width = \"0.0005\" />" %( float(BL.qstart)*Scale_factor, (old_counter+10),    (int(BL.qend)-int(BL.qstart))*Scale_factor, "tomato")

				print "<text x=\"%f\" y=\"%i\" transform=\"rotate(270,%f,%i)\" font-size=\"40\" >%s</text>" %((float(BL.qstart))*Scale_factor+readable,(old_counter+12),float(BL.qstart)*Scale_factor+readable,(old_counter+12),BL.gene)


			Last_Anch=float(BL.qstart)*Scale_factor+readable
		#Statement to print line connencting offset text if it is outside the boundaries of the box.
			if (int(BL.qend)-int(BL.qstart))*Scale_factor+BL.qstart*Scale_factor < (float(BL.qstart))*Scale_factor+readable and Comp <=Text_spacer: # for skinny boxes draw line to text
				print "<line x1=\"%i\" y1=\"%i\" x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"01\" stroke-opacity = \"0.7\" />" %(float(BL.qstart)*Scale_factor+(((int(BL.qend)-int(BL.qstart))*Scale_factor)/1.0),  old_counter-10 , float(BL.qstart)*Scale_factor+readable, old_counter-12)                                              
		BL=Contig[0]
		print "<line x1=\"0\" y1=\"%i\" x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"10\"/>" %(old_counter, int(BL.qlen)*Scale_factor  , old_counter)
		print  "<text x=\"%i\" y=\"%i\" font-size=\"40\" >%s                        </text>" %(int(BL.qlen)*Scale_factor+10,(old_counter),BL.qseqid)
		
		for X in range(0,BL.qlen,1000):
			print"<line x1=\"%i\" y1=\"%i\"  x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"2\"/>" %(X*Scale_factor,old_counter+2 ,X*Scale_factor, old_counter)		
		for X in range(0,BL.qlen,5000):
			print"<line x1=\"%i\" y1=\"%i\"  x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"5\"/>" %(X*Scale_factor,old_counter+4 ,X*Scale_factor, old_counter)
		for X in range(0,BL.qlen,10000):
			print"<line x1=\"%i\" y1=\"%i\"  x2=\"%i\" y2=\"%i\" stroke=\"black\" stroke-width = \"10\"/>" %(X*Scale_factor,old_counter+8 ,X*Scale_factor, old_counter)
		print "</g>"
		if BL.qstart > BL.qend:
			print "ERROR"
		old_counter+=1500
		

print "</svg>"
#		












