#!/usr/bin/python

#written using svg 






import argparse


class SVGRect:
	def __init__(self, XPOS, YPOS, height, width, R,G,B ):
		self.XPOS=XPOS
		self.YPOS=YPOS
		self.height=height
		self.width=width
		self.R=R
		self.G=G
		self.B=B

class HSLCol:
	def __init__(self, Name, Values):
		self.Name=Name
		self.Values=Values

		

def GradientMaker(MinColor, MaxColor, Value,Max_Value):
		#function to create gradient between 2 colors.
		if MinColor >MaxColor and Value !=0:
			BColor=MaxColor+(MinColor-MaxColor)*(float(Value)/float(Max_Value))
			BColor=255-BColor
		elif MinColor <MaxColor and Value !=0:
			BColor=MinColor+(MaxColor-MinColor)*(float(Value)/float(Max_Value))
#			print "Min Used"              
			
		elif Value==0:
			BColor=MinColor
		else :
			BColor=MaxColor
		
		return int(BColor)


def HeatMapColor(Value, RangeList, ColorList,ColorDict):
		#box_color=[R,G,B] percetages Here default color is white if not in range etc..
		box_color=[0,0,0] #black for default in HSL
		for RANGE, COLOR in zip(RangeList, ColorList):
			if Value >= RANGE[0] and Value < RANGE[1]:
				box_color=[]
				OldColor=ColorDict[COLOR.Name]
				
				for MinC,MaxC in zip(OldColor.Values,COLOR.Values):
					Element=GradientMaker(MinC, MaxC, Value,RANGE[1])
					box_color.append(Element)
		return box_color

parser=argparse.ArgumentParser()
parser.add_argument("CSV", help="File of properly sorted elements in csv format.")
parser.add_argument("Config", help="File with color values, ranges and order in proper format.\n\tFormat= space delimited,[ColorName] [Rvalue] [GValue] [BValue] [StartRange] [EndRange which must equal previous start range]\n\tEx:\tYellow 255 255 0 1.5 4\n\t\tWhite 255 255 255 4 1000")
parser.add_argument("OUT", help="File name for output svg. Must end in svg" )



args=parser.parse_args()


CF=open(args.Config,"r")
Config=CF.read()
Config=Config.split("\n")
ColorDict={}
ColorList=[]
RangeList=[]

#below are defaults in case they are not provided in config file.
font=12
boxSize=15
xMargin=500
yMargin=500
textOffset=150
width=120
height=1000

for Element in Config:
	Element=Element.split("=")
	if "#" in Element[0]:
		pass
	elif "#" not in Element[0]:
		if Element[0]=="color":
			Color=Element[1].split(" ")
			if len(ColorList)==0:
				Message=" must have have exactly 6 fields in for Color variable, separated by a space."
				assert(len(Color)==6) , Message
				COL=HSLCol(Color[0],[float(Color[1]),float(Color[2]),float(Color[3])])
				ColorList.append(COL)
				RangeList.append([float(Color[4]),float(Color[5])])
				ColorDict[Color[0]]=COL 
			elif len(ColorList) >0 :
				COL=HSLCol(Color[0],[int(Color[1]),int(Color[2]),int(Color[3])])
				ColorDict[Color[0]]=ColorList[-1] 
				ColorList.append(COL)
				RangeList.append([float(Color[4]),float(Color[5])])
		elif Element[0]=="font":
			fontSize=float(Element[1])
		elif Element[0]=="boxSize":
			boxSize=float(Element[1])
		elif Element[0]=="xMargin":
			xMargin=float(Element[1])
		elif Element[0]=="yMargin":
			yMargin=float(Element[1])
		elif Element[0]=="textOffset":
			textOffset=float(Element[1])
		elif Element[0]=="width":
			width=float(Element[1])
		elif Element[0]=="height":
			height=float(Element[1])

#print height, width, textOffset, yMargin, xMargin, boxSize, fontSize ,"\n\t",ColorDict

#for X in ColorList:
#	print X.Name, X.Values

			#ColorDict={"Pink":Blue, "Yellow":Pink, "Blue":Base,}
#ColorList=[Blue,Pink, Yellow]
#RangeList=[[0,.25],[.25,1.0],[1.0,3.0]]
			

##Yellow=HSLCol("Yellow",[255,255,0]) Bold Yellow
#Base=HSLCol("Base",[0,0,0])
#Blue=HSLCol("Blue",[0,0,128])
#Pink=HSLCol("Pink",[225,0,255])
#White=HSLCol("White", [255,255,255] )
#Yellow=HSLCol("Yellow", [254,249,89] ) # more subtle.






Message= "Output file must end in .svg"
assert(args.OUT[-4:]==".svg"),Message

f=open(args.CSV,"r")

DS=f.read()
DSs=DS.split("\n")

TheMatrix=[]
Header=[]
RowLabel=[]
Xindex=[]
Yindex=[]
del DS
counter=0
LENGTH = len(DSs[0].split(","))
for X in range(LENGTH):
	Xindex.append(X)
for Line in DSs :

	DSt=Line.split(",")
	if len(DSt) >1:
		Message="All rows must have the same number of Columns.\n Offending Line No"+str(counter)+" \n\t"+Line
		assert( LENGTH==len(DSt)),Message
		if counter==0:
			TheMatrix.append(DSt)
			counter+=1
			
		else:
			tmpRow=[]
			tmpRow.append(DSt[0])
			for X in DSt[1:]:
				tmpRow.append(float(X))
			
			TheMatrix.append(tmpRow)
			counter+=1
#			
#print TheMatrix
HeatMap=TheMatrix
View_Max=width

Counter=0
OldCounter=10
BoxSize=boxSize
XCounter=xMargin
YCounter=yMargin
FontSize=font

Header="""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%ipt" height="%ipt" viewBox="-50 0 %i %i" version="1.1">
""" %(len(HeatMap[0])*BoxSize+2*XCounter,len(HeatMap[0])*BoxSize+2*XCounter, len(HeatMap[0])*BoxSize+2*XCounter,len(HeatMap[0])*BoxSize+2*YCounter)
##print Header
		
		
f=open(args.OUT,'w')
f.write("")
f.close()
f=open(args.OUT,'a')
f.write(Header)

#Back up color 
##Yellow=HSLCol("Yellow",[255,255,0]) Bold Yellow
#Base=HSLCol("Base",[0,0,0])
#Blue=HSLCol("Blue",[0,0,128])
#Pink=HSLCol("Pink",[225,0,255])
#White=HSLCol("White", [255,255,255] )
#Yellow=HSLCol("Yellow", [254,249,89] ) # more subtle.
#ColorDict={"Pink":Blue, "Yellow":Pink, "Blue":Base,}
#ColorList=[Blue,Pink, Yellow]
#RangeList=[[0,.25],[.25,1.0],[1.0,3.0]]









HeatMapBoxes=[]
for Row in HeatMap:
	BoxRow=[]
	XCounter=xMargin
	if YCounter==yMargin: # first line will be treated as headers.
		f.write("<g>\n")
		for Element in Row:
			X_TextPos=float(XCounter+float(BoxSize)/2.0)
			Y_TextPos=YCounter+BoxSize
			f.write("<text x=\"%f\" y=\"%i\" transform=\"rotate(270,%f,%i)\" font-size=\"%i\" >%s</text>" %(X_TextPos,Y_TextPos,X_TextPos,Y_TextPos,FontSize,Element))
			XCounter+=BoxSize
		f.write("</g>\n")
	elif YCounter >yMargin :
		f.write("<g>\n")
		X_TextPos=XCounter-150
		Y_TextPos=YCounter+BoxSize
		print X_TextPos,Y_TextPos,X_TextPos,Y_TextPos,FontSize,Row[0]
		f.write("<text x=\"%f\" y=\"%i\"  font-size=\"%i\" >%s</text>" %(X_TextPos,Y_TextPos,FontSize,Row[0]))# assumes first column of every row is a label
		XCounter+=BoxSize
		for Element in Row[1:]:
			Color=HeatMapColor(Element,RangeList,ColorList,ColorDict)
			Box=SVGRect(XCounter, YCounter, BoxSize, BoxSize, Color[0],Color[1],Color[2])
			print Box.XPOS, Box.YPOS,Box.R, Box.G, Box.B
			XCounter+=BoxSize
			f.write(" <rect x=\""+str(Box.XPOS)+"\" y=\""+str(Box.YPOS)+"\" width=\""+str(BoxSize)+"\" height=\""+str(BoxSize)+"\" style=\"fill:rgb(%i,%i,%i);stroke-width:0;stroke:rgb(0,0,0)\" />\n" %(Color[0],Color[1],Color[2]))
		f.write("</g>\n")
	YCounter+=BoxSize

f.write("</svg>")
f.close()
