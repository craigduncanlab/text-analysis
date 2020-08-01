import sys
import review # this uses xmlutil as well
# coverpage - docx legal docs classifier
# (c) Craig Duncan 2020
# 

# test if first page is likely to be a document coverpage
def parseCoverPage(filepath):
	plist=getFirst50(filepath) # first 50 lines
	subset=firstpage_analysis(plist)
	result=testcoverpage(subset)
	if result==True:
		return True
	else:
		return False
		
def getFirst50(filepath):
	myparastats=review.openfilestyles(filepath)
	plist=myparastats[0:50]
	return plist

def checkCourtDoc(plist):
	#print("Checking Court Doc")
	courtList=["In the Matter of ","Court","plaintiff","defendant","applicant","respondent","registry","Affidavit","Summons","CIV","Writ"]
	return classifyCoverPage(plist,courtList)

def checkLegalDoc(plist):
	#print("Checking Legal Doc")
	docList=["Between","Parties","It is agreed","agreement"]
	result=classifyCoverPage(plist,docList)
	if result==False:
		result2=checkLegalDocTitles(plist)
		if result2==True:
			#print("Found legal doc (by title)")
			return True
	return False

# first 50 lines will usually include front page as well
# taking in the next page will help push score over if needed
def checkLegalDocTitles(plist):
	#print("Checking Legal Doc Titles")
	docList=["Agreement to Lease","Lease","Assignment of Lease", "Joint Venture", "Partnership Deed", "Constitution", "Mortgage", "Deed of ", "Contract of","Consulting Agreement", "Distribution Agreement"]
	result=classifyCoverPage(plist,docList)
	return result

# simple test to determine if Court document or not
def classifyCoverPage(plist,testList):
	courtrank=0
	count=0
	for i in plist:
		count=count+1
		text=i[0]
		#print(text)
		#words=text.split(' ')
		for x in testList:
			#don't worry about case
			tx=text.lower().strip()
			xx=x.lower().strip()
			if tx.find(xx)!=-1:
				# print(x,text)
				courtrank=courtrank+1
	result=float(courtrank/count*100)
	#print("Stats")
	#print(courtrank,count)
	# If Court words score > 5% then we accept it is Court doc
	if result>5:
		#print("This is the check document. Score %s" % result)
		return True
	else:
		#print("Not the checked document. Score %s" % result)
		return False

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
	lm=len(mainlist)
	if lm>0:
		for i in mainlist:
			text=i[0]
			words=i[2]
			#print(text)
			# mylist.append(i[0]) # text
			total=total+words # density
			if words<3:
				lowcount=lowcount+1 # less than 3 words in line
		print("Total word density: %d" % total)
		ave=float(total/lm)
		percentlow=float(lowcount/lm*100)
		print("Ave word density: %f" % ave)
		print("Low word line pc %f" % percentlow)
		if total<50 or ave<3 or percentlow>75:
			print("Coverpage")
			return True
		else:
			print("Not coverpage")
	return False

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
			parseCoverPage(nbname)
		else:
			print("This program requires .docx filename and search word i.e. python3 findphrase.py myfile.docx GST")
			print("Case sensitive.  Include phrases in quotes.  Use ? to findall")
	else:
		doError()