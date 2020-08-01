import sys
import review # this uses xmlutil as well
# divisions - docx legal docs segmentation
# (c) Craig Duncan 2020
# 

# test if first page is likely to be a document coverpage
def parseCoverPage(filepath):
	myparastats=review.openfilestyles(filepath)

	print("====FIRST PAGE===")
	plist=myparastats[0:50] # first 50 lines
	subset=firstpage_analysis(plist)
	result=testcoverpage(subset)
	if result==True:
		classifyCoverPage(plist)

# simple test to determine if Court document or not
def classifyCoverPage(plist):
	courtList=["Court","plaintiff","defendant","applicant","respondent","registry"]
	courtrank=0
	for i in plist:
		text=plist[0]
		words=text.split(' ')
		for x in courtList:
			if x in words:
				count=count+1
				courtrank=courtrank+1
	result=float(count/courtrank)
	if result>0.8:
		print("This is a Court document")
		exit()
	else:
		print("Not a Court document")
		exit()


# a utility function that works with the review.py
# inputs: 
# rollave is:
# array with [text item,style,index (sentences),density,words,chars,outline level,pbreak,sbreak]
# it requires generation of 'sentence list' from the docx document using review.py
# 'request' is the search phrase

def doDivisionAnalysis(filepath):
	myparastats=review.openfilestyles(filepath)
	# sentences do not include blank lines
	sentencelist=review.getSentenceObjects(myparastats)

	rollave=review.getRollAve(sentencelist)
	# test analsis for the 'rlease.docx'

	#---- these are all analysis where we also use rollave
	print("---====DIVISION ANALYSES===---")
	print("---Analyse the main divisions in the document---")
	
	body_analysis(rollave,10)
	title_analysis(rollave)
	# print("----roll those density dots-------")
	# review.rolldensitydots(rollave)
	
# inputs: for measuring paras: about 7
# for measuring sentences: about 
def body_analysis(rollave, threshold):
	print("---BODY ANALYSIS---")
	print("----Filter doc for high word density---")
	filterlist=[]
	for item in rollave:
		density=item[3]
		if (density>threshold):
			filterlist.append(item)
	divisionanalysis(filterlist)

def title_analysis(rollave):
	print("---TITLE ANALYSIS---")
	print("----Filter doc for high word density---")
	filterlist=[]
	for item in rollave:
		density=item[3]
		if (density<10):
			filterlist.append(item)
	print(filterlist) #text,style,index,density
	#exit()
	divisionanalysis(filterlist)

# pre-req: find a region that appears to be a 'coverpage'
# i.e. do a rolling low density test for 100 lines or so
# for now, use first 50 lines in document (some old docs could be at end)
# then use this function to decide where page ends
def firstpage_analysis(plist):
	print("---COVERPAGE ANALYSIS---")
	#print("----Filter doc for low word density and low word count ---")
	filterlist=[]
	mainlist=[]
	breakmax=0
	pageend=0
	blocktext=0
	for item in plist:
		tester=item[0][0:4]
		#if (tester=="COMM" and item[1]!="TOC1"):
			#print(item)
			#exit()
		text=item[0]
		style=item[1]
		prefix=style[0:3]
		words=item[2]
		sentences=item[3]
		index=item[4]
		density=item[5]
		pbreak=item[7]
		sbreak=item[8]
		#if(style=="TOC1"):
		#	print(prefix)
		# Forced page end: if we find an unusual block of text treat it as end of page
		#if (len(text)>100):
		#	blocktext=1
		if pbreak==1 or sbreak==1 or blocktext==1:
			pageend=1
			if breakmax==0:
				breakmax=index
				print(" --- page break found ---")
			
		# filter not used
		if (density<8 and words<8):
			# can we rely on title names? or just word count?
			#if (style=="Normal" or style=="Title" and words<8):
			if (prefix!="TOC" and pageend!=1):
				filterlist.append(item)
	if breakmax==0:
		breakmax=len(plist)
	mainlist=plist[0:breakmax] #:breakmax]
	return mainlist

def testcoverpage(mainlist):
	total=0
	lowcount=0
	for i in mainlist:
		text=i[0]
		words=i[2]
		print(text)
		# mylist.append(i[0]) # text
		total=total+words # density
		if words<3:
			lowcount=lowcount+1 # less than 3 words in line
	print("Total word density: %d" % total)
	ave=float(total/len(mainlist))
	percentlow=float(lowcount/len(mainlist)*100)
	print("Ave word density: %f" % ave)
	print("Low word line pc %f" % percentlow)
	if total<50 or ave<3 or percentlow>75:
		print("Coverpage")
		return True
	else:
		print("Not coverpage")
	return False

def TOC_analysis(rollave):
	print("---TOC ANALYSIS---")
	print("----Filter doc for low word density---")
	filterlist=[]
	for item in rollave:
		density=item[3]
		words=item[4]
		style=item[1]
		prefix=style[0:2]
		if (density<5 and words<12):
			# can we rely on title names? or just word count?
			#if (style=="Normal" or style=="Title" and words<8):
			if (prefix=="TOC"):
				filterlist.append(item)
	print(filterlist) #text,style,index,density
	#exit()
	divisionanalysis(filterlist)


# inputs: rollave is a list of word density, text, paragraph index
# inputs: filtered[mtext,mstyle,mindex,density,mwords,mchars,molevel,pbreak,sbreak]
# function (transform): if there's a big gap in text, assume next section?
# outputs: list of divisions
def divisionanalysis(filterlist):
	divisions=[]
	gap=10 # I used 5 when checking paragraphs not sentences
	print("---Checking divisions---")
	count=0
	min=0
	prev=0
	for p in filterlist:
		index=p[2]
		pbreak=p[7]
		sbreak=p[8]
		print(index)
		if (min==0):
			min=index
		if (index>0):
			if (index-prev>gap or sbreak==1): #break on every 'section break'
				divisions.append(index) # record any breaks in para flow (jumps)
				prev=index
			else:
				prev=index
	print("---Reporting index numbers of divisions---")
	print("Number of divisions: %d" % len(divisions))
	for div in divisions:
		print (div)
	divcount=0
	masterlist=[]
	currentdiv=[]
	stopindex=0
	if len(filterlist)>0:
		stopindex=filterlist[len(filterlist)-1][2]
	marker=0
	#make division lists ready for markup
	for p in filterlist:
		index=p[2]
		if (marker!=stopindex):
			marker=divisions[divcount]
		if (index<marker):
			text=p[0] #[mtext,mstyle,mindex,density]
			style=p[1]
			index=p[2]
			store=[text,style,index] # loses density?
			currentdiv.append(store)
			print(store)
		#print(currentdiv)
		if (index==marker):
			print("---division break %d at %d ----" % (divcount,marker))
			print()
			print()
			print(index)
			if(len(currentdiv)>0):
				masterlist.append(currentdiv)
				currentdiv=[]
			if (divcount<(len(divisions)-1)):
				divcount=divcount+1 
			else:
				marker=stopindex
		#print(p)
		#currentdiv.append(p)
	dc=1
	for y in masterlist:
		print("-------div---------")
		fname="masterlist_div"+str(dc)
		print(fname)
		#print(y)
		# convertToMarkdown(y,fname) # each y is a currendiv list of paragraphs.  Performs save?
		dc=dc+1

# START HERE
# nb make any import files also conditional on being main...
args=len(sys.argv)
print(args)
# if this is run as the top-level stand-alone program with 1 parameter
if (args==2 and __name__ == '__main__'):
	nbname=sys.argv[1]
	# request=sys.argv[2]
	if len(nbname)!=0:
		# remainder is optional for now:
		#
		nameonly,suffix=nbname.split('.')
		if (suffix=="docx"):
			print("Review file name is "+nbname)
			#doDivisionAnalysis(nbname)
			parseCoverPage(nbname)
		else:
			print("This program requires .docx filename and search word i.e. python3 findphrase.py myfile.docx GST")
			print("Case sensitive.  Include phrases in quotes.  Use ? to findall")
	else:
		doError()